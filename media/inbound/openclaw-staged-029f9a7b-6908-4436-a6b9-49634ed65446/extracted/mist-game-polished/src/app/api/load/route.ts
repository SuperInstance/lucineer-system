import { db } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    const playerName = request.nextUrl.searchParams.get("name") || "Puppy";

    const save = await db.gameSave.findFirst({
      where: { playerName },
    });

    if (!save) {
      return NextResponse.json({ success: true, data: null });
    }

    return NextResponse.json({
      success: true,
      data: {
        playerName: save.playerName,
        currentWorld: save.currentWorld,
        playerPos: { x: save.playerX, y: save.playerY },
        discoveries: JSON.parse(save.discoveries),
        stickers: JSON.parse(save.stickers),
        xp: save.xp,
        level: save.level,
        teachingsSeen: JSON.parse(save.teachingsSeen),
        worldCompleted: JSON.parse(save.worldCompleted),
      },
    });
  } catch (error) {
    console.error("Load failed:", error);
    return NextResponse.json(
      { success: false, error: "Load failed" },
      { status: 500 }
    );
  }
}