/**
 * Cloudflare Worker for OpenClaw Integration
 *
 * This worker provides:
 * - HTTP endpoint for OpenClaw agent communication
 * - Cloudflare Workers AI integration
 * - Request/response handling for Telegram agents
 * - Environment-based configuration
 */

export default {
  async fetch(request, env, ctx) {
    try {
      // Handle CORS
      if (request.method === 'OPTIONS') {
        return new Response(null, {
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          },
        });
      }

      const url = new URL(request.url);
      const path = url.pathname;

      // Health check endpoint
      if (path === '/health') {
        return Response.json({
          status: 'ok',
          service: 'openclaw-cloudflare-worker',
          timestamp: new Date().toISOString(),
          features: {
            workers_ai: !!env.AI,
            kv: !!env.KV,
            durable_objects: !!env.DURABLE_OBJECTS
          }
        });
      }

      // OpenClaw proxy endpoint
      if (path === '/proxy' && request.method === 'POST') {
        return await handleOpenClawProxy(request, env, ctx);
      }

      // Workers AI endpoint
      if (path === '/ai' && request.method === 'POST') {
        return await handleWorkersAI(request, env, ctx);
      }

      // Telegram webhook endpoint
      if (path === '/telegram' && request.method === 'POST') {
        return await handleTelegramWebhook(request, env, ctx);
      }

      // Default 404
      return new Response('Not Found', { status: 404 });

    } catch (error) {
      return Response.json({
        error: 'Internal Server Error',
        message: error.message,
        stack: error.stack
      }, { status: 500 });
    }
  }
};

/**
 * Handle OpenClaw proxy requests
 */
async function handleOpenClawProxy(request, env, ctx) {
  try {
    const body = await request.json();

    // Forward to OpenClaw gateway
    const gatewayUrl = 'http://127.0.0.1:18789';
    const response = await fetch(`${gatewayUrl}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('Authorization') || `Bearer ${env.OPENCLAW_TOKEN || 'default-token'}`
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    return Response.json({
      success: response.ok,
      data: data,
      proxy: 'cloudflare-worker',
      timestamp: new Date().toISOString()
    }, { status: response.status });

  } catch (error) {
    return Response.json({
      error: 'Proxy Error',
      message: error.message
    }, { status: 500 });
  }
}

/**
 * Handle Cloudflare Workers AI requests
 */
async function handleWorkersAI(request, env, ctx) {
  try {
    if (!env.AI) {
      return Response.json({
        error: 'Workers AI not configured',
        message: 'Set AI binding in wrangler.toml'
      }, { status: 500 });
    }

    const body = await request.json();
    const { model, messages, max_tokens, temperature } = body;

    const response = await env.AI.run(model || '@cf/meta/llama-3.1-8b-instruct', {
      messages: messages || [{ role: 'user', content: 'Hello!' }],
      max_tokens: max_tokens || 512,
      temperature: temperature || 0.7
    });

    return Response.json({
      response: response,
      provider: 'cloudflare-workers-ai',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    return Response.json({
      error: 'Workers AI Error',
      message: error.message
    }, { status: 500 });
  }
}

/**
 * Handle Telegram webhook requests
 */
async function handleTelegramWebhook(request, env, ctx) {
  try {
    const body = await request.json();

    // Store in KV if available
    if (env.KV) {
      await env.KV.put(`telegram:${Date.now()}`, JSON.stringify(body), {
        expirationTtl: 86400 // 24 hours
      });
    }

    // Forward to OpenClaw gateway
    const gatewayUrl = 'http://127.0.0.1:18789';
    const response = await fetch(`${gatewayUrl}/telegram/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    return Response.json({
      success: response.ok,
      webhook: 'telegram',
      timestamp: new Date().toISOString()
    }, { status: response.status });

  } catch (error) {
    return Response.json({
      error: 'Webhook Error',
      message: error.message
    }, { status: 500 });
  }
}