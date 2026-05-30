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
require("lazy").setup("plugins")
require("configs.keymaps")
vim.opt.number = true
vim.opt.conceallevel = 2
vim.opt.concealcursor = ""

-- Didn't know this option I had to do "+y
-- Where have you beeennnnn!!!
vim.opt.clipboard:append('unnamedplus')
vim.opt.background = 'dark'

vim.keymap.set("n", "<leader>u", function()
  vim.cmd("call UltiSnips#RefreshSnippets()")
end, { desc = "Refresh UltiSnips" })



