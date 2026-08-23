import { db } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      playerName = "Puppy",
      currentWorld,
      playerPos,
      discoveries,
      stickers,
      xp,
      level,
      teachingsSeen,
      worldCompleted,
    } = body;

    // Upsert: find existing save or create new
    const existing = await db.gameSave.findFirst({
      where: { playerName },
    });

    if (existing) {
      await db.gameSave.update({
        where: { id: existing.id },
        data: {
          currentWorld,
          playerX: playerPos?.x ?? 5,
          playerY: playerPos?.y ?? 10,
          discoveries: JSON.stringify(discoveries ?? []),
          stickers: JSON.stringify(stickers ?? []),
          xp: xp ?? 0,
          level: level ?? 0,
          teachingsSeen: JSON.stringify(teachingsSeen ?? []),
          worldCompleted: JSON.stringify(worldCompleted ?? []),
        },
      });
    } else {
      await db.gameSave.create({
        data: {
          playerName,
          currentWorld: currentWorld ?? "farm",
          playerX: playerPos?.x ?? 5,
          playerY: playerPos?.y ?? 10,
          discoveries: JSON.stringify(discoveries ?? []),
          stickers: JSON.stringify(stickers ?? []),
          xp: xp ?? 0,
          level: level ?? 0,
          teachingsSeen: JSON.stringify(teachingsSeen ?? []),
          worldCompleted: JSON.stringify(worldCompleted ?? []),
        },
      });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Save failed:", error);
    return NextResponse.json(
      { success: false, error: "Save failed" },
      { status: 500 }
    );
  }
}