vim.g.mapleader = " "
vim.g.maplocalleader = " "
vim.g.python3_host_prog = "~/.config/nvim/py/bin/python"

-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    {
      "lervag/vimtex",
      lazy = false,
      init = function()
        vim.g.vimtex_view_method = "zathura"
        vim.g.tex_conceal = "abdmg"
	   vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI" }, {
            pattern = "*.tex",
            callback = function()
                vim.cmd("silent! write")
            end,
        })
      end,
    },
    {
    'nvim-telescope/telescope.nvim', version = '*',
    dependencies = {
        'nvim-lua/plenary.nvim',
        -- optional but recommended
        { 'nvim-telescope/telescope-fzf-native.nvim', build = 'make' },
    }
},
{
  "frabjous/knap",
  config = function()
    -- settings
    -- keymaps
    local knap = require("knap")
    local opts = { silent = true }

    vim.keymap.set({ "n", "v", "i" }, "<F4>", function() knap.process_once() end, opts)
    vim.keymap.set({ "n", "v", "i" }, "<F6>", function() knap.close_viewer() end, opts)
    vim.keymap.set({ "n", "v", "i" }, "<F7>", function() knap.toggle_autopreviewing() end, opts)
    vim.keymap.set({ "n", "v", "i" }, "<F8>", function() knap.forward_jump() end, opts)
  end,
},
    {
  "pxwg/math-conceal.nvim",
  event = "VeryLazy",
  main = "math-conceal",
  --- @type LaTeXConcealOptions
  opts = {
    conceal = {
      "greek",
      "script",
      "math",
      "font",
      "delim",
      "phy",
    },
    ft = { "plaintex", "tex", "context", "bibtex", "markdown", "typst" },
  },
},
    {
      "m4xshen/hardtime.nvim",
      lazy = false,
      dependencies = { "MunifTanjim/nui.nvim" },
      opts = {},
    },
    {

  'chomosuke/typst-preview.nvim',

  lazy = false, -- or ft = 'typst'

  version = '1.*',

  opts = {}, -- lazy.nvim will implicitly calls `setup {}`

},
{
  "vimwiki/vimwiki",
  lazy = false,
  priority = 1000,  -- Load first
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

  "mason-org/mason.nvim",

  opts = {

    ensure_installed = {

      "tinymist",
      "pyright"

    },

  },

},
{
  "tools-life/taskwiki",
  lazy = false,
  priority = 900,  -- Load after vimwiki
  dependencies = {
    "vimwiki/vimwiki",
    "powerman/vim-plugin-AnsiEsc",
  },
  init = function()
    -- Ensure taskwiki uses the correct Python
    vim.g.taskwiki_disable_concealcursor = 1
  end,
},   {
      'stevearc/oil.nvim',
      opts = {},
      dependencies = { { "echasnovski/mini.icons", opts = {} } },
      lazy = false,
    },
    
{
  "olimorris/codecompanion.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-treesitter/nvim-treesitter",
  },
  opts = {
    strategies = {
      chat = {
        adapter = "openai",
      },
    },

    opts = {
      log_level = "DEBUG",
    },
  },
},
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
  install = { colorscheme = { "habamax" } },
  checker = { enabled = true },
})
vim.opt.number = true
vim.opt.conceallevel = 2
vim.opt.concealcursor = ""
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, { desc = 'Telescope find files' })
vim.keymap.set('n', '<leader>fg', builtin.live_grep, { desc = 'Telescope live grep' })
vim.keymap.set('n', '<leader>fb', builtin.buffers, { desc = 'Telescope buffers' })
vim.keymap.set('n', '<leader>fh', builtin.help_tags, { desc = 'Telescope help tags' })
vim.keymap.set("n", "<leader>u", function()
  vim.cmd("call UltiSnips#RefreshSnippets()")
end, { desc = "Refresh UltiSnips" })

