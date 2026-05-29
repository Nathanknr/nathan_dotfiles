return {
  "nvim-telescope/telescope.nvim",
  version = "*",

  dependencies = {
    "nvim-lua/plenary.nvim",

    -- Faster fuzzy matching (optional but recommended)
    {
      "nvim-telescope/telescope-fzf-native.nvim",
      build = "make",
    },
  },

  config = function()
    local telescope = require("telescope")
    local builtin = require("telescope.builtin")

    telescope.setup({
      defaults = {
        -- you can tweak layout here
        layout_config = {
          horizontal = { preview_width = 0.55 },
        },
      },
    })

    -- Keymaps (plugin-specific)
    vim.keymap.set("n", "<leader>ff", builtin.find_files, { desc = "Find files" })
    vim.keymap.set("n", "<leader>fg", builtin.live_grep, { desc = "Live grep" })
    vim.keymap.set("n", "<leader>fb", builtin.buffers, { desc = "Buffers" })
    vim.keymap.set("n", "<leader>fh", builtin.help_tags, { desc = "Help tags" })
    vim.keymap.set("n", "<leader>fc", builtin.commands, { desc = "Commands" })
  end,
}
