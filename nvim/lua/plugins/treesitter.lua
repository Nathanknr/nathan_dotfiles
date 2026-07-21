return {
	"nvim-treesitter/nvim-treesitter",
	build = ":TSUpdate",
	lazy = false,
	config = function()
		require("nvim-treesitter").setup({
			ensure_installed = {
				"bash",
				"c",
				"html",
				"lua",
				"css",
				"javascript",
				"markdown",
				"vim",
				"vimdoc",
			},
			ignore_install = { "latex" }, -- never auto-install latex parser

			auto_install = true,
			highlight = { enable = true, disable = { "latex" } },
			indent = { enable = true, disable = { "latex" } },
		})
	end,
}
