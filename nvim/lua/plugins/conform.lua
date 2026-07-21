return {
  {
    "stevearc/conform.nvim",
    opts = {
      notify_on_error = false,

      format_on_save = {
        timeout_ms = 500,
        lsp_fallback = true,
      },

      formatters_by_ft = {
        lua = { "stylua" },

        python = {
          "ruff_organize_imports",
          "ruff_format",
        },

        javascript = {
          "prettierd",
          "prettier",
        },

        html = {
          "prettierd",
          "prettier",
        },

        css = {
          "prettierd",
          "prettier",
        },
      },
    },
  },

  {
    "windwp/nvim-ts-autotag",
    opts = {},
  },
}
