return {
	{
		"lervag/vimtex",
		lazy = false,
		init = function()
			vim.g.vimtex_view_method = "zathura"
			vim.g.vimtex_syntax_enabled = 1
			vim.g.vimtex_syntax_conceal_disable = 0

			local save_timer = vim.uv.new_timer() -- create once, reuse forever
			vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI" }, {
				pattern = "*.tex",
				callback = function()
					save_timer:stop() -- cheap, just resets the timer's internal state
					save_timer:start(
						500,
						0,
						vim.schedule_wrap(function()
							vim.cmd("silent! write")
						end)
					)
				end,
			})
		end,
	},
	{
		"tools-life/taskwiki",
		lazy = false,
		dependencies = { "vimwiki/vimwiki" },
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
	--{
	--	"vimwiki/vimwiki",
	--	lazy = false,
	--	priority = 1000, -- Load first
	--	init = function()
	--		vim.g.vimwiki_list = {
	--			{
	--				path = "~/vimwiki/",
	--				syntax = "default",
	--				ext = ".wiki",
	--			},
	--		}
	--	end,
	--},
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
