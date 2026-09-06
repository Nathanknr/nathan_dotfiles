return {
	{
		"mason-org/mason.nvim",
		opts = {},
	},
	{
		"neovim/nvim-lspconfig",
		config = function()
			vim.diagnostic.config({
				virtual_text = true,
			})
		end,
	},
	{
		"mason-org/mason-lspconfig.nvim",
		opts = {
			ensure_installed = {
				"rust_analyzer",
				"pyright",
				"lua_ls",
			},
			automatic_enable = true,
		},
	},
}
