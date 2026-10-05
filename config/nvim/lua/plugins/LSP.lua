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
			vim.lsp.config("tinymist", {
				settings = {
					formatterMode = "typstyle",
					exportPdf = "onType", -- or "onSave"
					semanticTokens = "disable",
				},
			})
		end,
	},
	{
		"mason-org/mason-lspconfig.nvim",
		opts = {
			ensure_installed = {
				"rust_analyzer",
				"pyright",
				"tinymist",
				"lua_ls",
			},
			automatic_enable = true,
		},
	},
}
