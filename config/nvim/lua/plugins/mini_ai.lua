return {
	"nvim-mini/mini.ai",
	version = "*",
	event = "VeryLazy",
	config = function()
		require("mini.ai").setup()
	end,
}
