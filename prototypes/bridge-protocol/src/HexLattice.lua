-- HexLattice.lua
-- Pure-Lua axial-coordinate hex grid for Slackwater / Roblox.
-- Compatible with standard Lua 5.1+ and Luau (Roblox).

local HexLattice = {}
HexLattice.__index = HexLattice

local DIRECTIONS = {
	{ q = 1,  r = 0  }, -- NE
	{ q = 1,  r = -1 }, -- E
	{ q = 0,  r = -1 }, -- SE
	{ q = -1, r = 0  }, -- SW
	{ q = -1, r = 1  }, -- W
	{ q = 0,  r = 1  }, -- NW
}

function HexLattice.new()
	local self = setmetatable({}, HexLattice)
	self.hexes = {}
	return self
end

function HexLattice:_key(q, r)
	return string.format("%d,%d", q, r)
end

function HexLattice:place(q, r, data)
	local key = self:_key(q, r)
	local hex = {
		q = q,
		r = r,
		data = data,
	}
	self.hexes[key] = hex
	return hex
end

function HexLattice:get(q, r)
	return self.hexes[self:_key(q, r)]
end

function HexLattice:remove(q, r)
	self.hexes[self:_key(q, r)] = nil
end

function HexLattice:neighbors(q, r)
	local result = {}
	for _, dir in ipairs(DIRECTIONS) do
		local nq, nr = q + dir.q, r + dir.r
		local neighbor = self:get(nq, nr)
		if neighbor then
			table.insert(result, neighbor)
		end
	end
	return result
end

function HexLattice:distance(aq, ar, bq, br)
	-- Axial distance on a hex grid.
	return (math.abs(aq - bq) + math.abs(aq + ar - bq - br) + math.abs(ar - br)) / 2
end

function HexLattice:all()
	local result = {}
	for _, hex in pairs(self.hexes) do
		table.insert(result, hex)
	end
	return result
end

function HexLattice:ring(centerQ, centerR, radius, fillData)
	-- Place a ring of hexes around a center. If fillData is a function, call it per hex.
	for q = -radius, radius do
		for r = math.max(-radius, -q - radius), math.min(radius, -q + radius) do
			if self:distance(centerQ, centerR, centerQ + q, centerR + r) == radius then
				local data = fillData
				if type(fillData) == "function" then
					data = fillData(centerQ + q, centerR + r)
				end
				self:place(centerQ + q, centerR + r, data)
			end
		end
	end
	return self
end

function HexLattice:disk(centerQ, centerR, radius, fillData)
	for q = -radius, radius do
		for r = math.max(-radius, -q - radius), math.min(radius, -q + radius) do
			local data = fillData
			if type(fillData) == "function" then
				data = fillData(centerQ + q, centerR + r)
			end
			self:place(centerQ + q, centerR + r, data)
		end
	end
	return self
end

return HexLattice
