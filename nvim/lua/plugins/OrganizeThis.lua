return {
	{
		"lervag/vimtex",
		lazy = false,
		init = function()
			vim.g.vimtex_view_method = "zathura"
			vim.g.tex_conceal = "abdmg"
			vim.g.vimtex_syntax_enabled = 1 -- keep vimtex's own syntax on
			vim.g.vimtex_syntax_conceal_disable = 0 -- keep conceal working

			local save_timer = nil

			vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI" }, {
				pattern = "*.tex",
				callback = function()
					if save_timer then
						save_timer:stop()
						save_timer:close()
					end
					save_timer = vim.uv.new_timer()
					save_timer:start(
						500,
						0,
						vim.schedule_wrap(function()
							vim.cmd("silent! write")
							save_timer:close()
							save_timer = nil
						end)
					)
				end,
			})
		end,
	},
	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {
			-- your configuration comes here
			-- or leave it empty to use the default settings
			-- refer to the configuration section below
		},
		keys = {
			{
				"<leader>?",
				function()
					require("which-key").show({ global = false })
				end,
				desc = "Buffer Local Keymaps (which-key)",
			},
		},
	},
	{
		"m4xshen/hardtime.nvim",
		lazy = false,
		dependencies = { "MunifTanjim/nui.nvim" },
		opts = {},
	},
	{

		"chomosuke/typst-preview.nvim",

		lazy = false, -- or ft = 'typst'

		version = "1.*",

		opts = {}, -- lazy.nvim will implicitly calls `setup {}`
	},
	{
		"vimwiki/vimwiki",
		lazy = false,
		priority = 1000, -- Load first
		init = function()
			vim.g.vimwiki_list = {
				{
					path = "~/vimwiki/",
					syntax = "default",
					ext = ".wiki",
				},
			}
		end,
	},
	{
		{
			"SirVer/ultisnips",
			event = "InsertEnter",
			lazy = false,
			init = function()
				vim.g.UltiSnipsSnippetDirectories = { "/home/nathan/.config/Ultisnips" }
				vim.g.UltiSnipsExpandTrigger = "<tab>"
				vim.g.UltiSnipsJumpForwardTrigger = "<tab>"
				vim.g.UltiSnipsJumpBackwardTrigger = "<C-k>"
				vim.g.UltiSnipsEditSplit = "vertical"
			end,
		},
	},
}
