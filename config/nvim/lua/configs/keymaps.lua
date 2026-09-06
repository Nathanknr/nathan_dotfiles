local map = vim.keymap.set
map("n", "<leader>jj", "<cmd>Oil<cr>")
map("i", "jk", "<Esc>")
map("i", "kj", "<Esc>")

vim.g.mapleader = " "

-- greatest remap ever
vim.keymap.set("x", "<leader>p", [["_dP]])
vim.keymap.set("n", "J", "mzJ`z")
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")
vim.keymap.set("n", "=ap", "ma=ap'a")

-- next greatest remap ever : asbjornHaland
vim.keymap.set({ "n", "v" }, "<leader>y", [["+y]])
vim.keymap.set("n", "<leader>Y", [["+Y]])

vim.keymap.set({ "n", "v" }, "<leader>d", '"_d')

vim.keymap.set("n", "<leader>l", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])
vim.keymap.set("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true })

vim.keymap.set("n", "<leader><leader>", function()
	vim.cmd("so")
end)

vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")

-- keymaps
vim.api.nvim_create_autocmd(
	"LspAttach",
	{ --  Use LspAttach auto command to only map the following keys after the language server attaches to the current buffer
		group = vim.api.nvim_create_augroup("UserLspConfig", {}),
		callback = function(ev)
			vim.bo[ev.buf].omnifunc = "v:lua.vim.lsp.omnifunc" -- Enable completion triggered by <c-x><c-o>

			local opts = function(desc)
				return { buffer = ev.buf, silent = true, desc = desc }
			end
			vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts("Go to definition"))
			vim.keymap.set("n", "<leader><space>", vim.lsp.buf.hover, opts("Hover documentation"))
			vim.keymap.set("n", "gi", vim.lsp.buf.implementation, opts("Go to implementation"))
			vim.keymap.set("n", "<leader>D", vim.lsp.buf.type_definition, opts("Go to type definition"))
			vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts("Rename symbol"))
			vim.keymap.set("n", "gr", vim.lsp.buf.references, opts("Find references"))

			-- vim.keymap.set({ "n", "v" }, "<leader>ca", function()
			-- 	require("tiny-code-action").code_action()
			-- end, opts("Code action"))
			vim.keymap.set("n", "<leader>o", vim.lsp.buf.format, opts("Format buffer"))

			vim.keymap.set("n", "<leader>d", function()
				vim.diagnostic.open_float({
					border = "rounded",
				})
			end, opts("Show diagnostics float"))
		end,
	}
)
