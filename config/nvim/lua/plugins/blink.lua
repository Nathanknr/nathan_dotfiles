return {
	-- Community snippet collection
	-- Your own snippets always take precedence if they use the same trigger.
	-----------------------------------------------------------------------------
	{
		"honza/vim-snippets",
	},

	-----------------------------------------------------------------------------
	-- Completion engine.
	--
	-- Responsibilities:
	--   • LSP completions
	--   • File path completions
	--   • Buffer word completions
	--   • Function signature help
	--
	-- NOTE:
	-- We intentionally DO NOT integrate UltiSnips with blink.cmp.
	-- Snippets are expanded manually using <Tab>, just as in a traditional
	-- UltiSnips workflow.
	-----------------------------------------------------------------------------
	{
		"Saghen/blink.cmp",
		version = "*",

		dependencies = {
			"Saghen/blink.lib",
		},

		opts = {
			-------------------------------------------------------------------------
			-------------------------------------------------------------------------
			keymap = {
				preset = "default",

				-- Accept the selected completion item.
				["<CR>"] = { "accept", "fallback" },

				-- Accept with Tab if the completion menu is visible.
				["<Tab>"] = { "accept", "fallback" },

				-- Show completion menu.
				["<S-Tab>"] = { "show" },

				-- Navigate completion menu.
				["<S-j>"] = { "select_next", "fallback" },
				["<S-k>"] = { "select_prev", "fallback" },
			},

			-------------------------------------------------------------------------
			-- Completion menu
			-------------------------------------------------------------------------
			completion = {
				menu = {
					auto_show = true,

					draw = {
						-- Use Treesitter to improve syntax highlighting.
						treesitter = { "lsp" },

						-- Menu layout.
						columns = {
							{
								"kind_icon",
								"label",
								"label_description",
								gap = 1,
							},
							{
								"kind",
							},
						},
					},
				},

				-- Automatically show documentation for the selected item.
				documentation = {
					auto_show = true,
				},
			},

			-------------------------------------------------------------------------
			-- Show function signatures while typing.
			-------------------------------------------------------------------------
			signature = {
				enabled = true,
			},

			-------------------------------------------------------------------------
			-- Use Lua fuzzy matching.
			-------------------------------------------------------------------------
			fuzzy = {
				implementation = "lua",
			},

			sources = {
				default = {
					"lsp", -- Language Server
					"path", -- File paths
				},

				providers = {
					lsp = {
						score_offset = 90,
					},
				},
			},
		},
	},
}
