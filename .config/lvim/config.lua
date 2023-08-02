
lvim.colorscheme = "catppuccin-mocha"
-- automatically install python syntax highlighting
lvim.builtin.treesitter.highlight.enable = true

lvim.builtin.treesitter.ensure_installed = {
  "python",
  "latex",
  "css",
  "bash",
  "cpp",
  "c"
}

-- Additional Plugins
table.insert(lvim.plugins, {
  "p00f/clangd_extensions.nvim",
})

vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "clangd" })

-- some settings can only passed as commandline flags, see `clangd --help`
local clangd_flags = {
  "--background-index",
  "--fallback-style=Google",
  "--all-scopes-completion",
  "--clang-tidy",
  "--log=error",
  "--suggest-missing-includes",
  "--cross-file-rename",
  "--completion-style=detailed",
  "--pch-storage=memory",     -- could also be disk
  "--folding-ranges",
  "--enable-config",          -- clangd 11+ supports reading from .clangd configuration file
  "--offset-encoding=utf-16", --temporary fix for null-ls
  -- "--limit-references=1000",
  -- "--limit-resutls=1000",
  -- "--malloc-trim",
  -- "--clang-tidy-checks=-*,llvm-*,clang-analyzer-*,modernize-*,-modernize-use-trailing-return-type",
  -- "--header-insertion=never",
  -- "--query-driver=<list-of-white-listed-complers>"
}

local provider = "clangd"

local custom_on_attach = function(client, bufnr)
  require("lvim.lsp").common_on_attach(client, bufnr)

  local opts = { noremap = true, silent = true, buffer = bufnr }
  vim.keymap.set("n", "<leader>lh", "<cmd>ClangdSwitchSourceHeader<cr>", opts)
  vim.keymap.set("x", "<leader>lA", "<cmd>ClangdAST<cr>", opts)
  vim.keymap.set("n", "<leader>lH", "<cmd>ClangdTypeHierarchy<cr>", opts)
  vim.keymap.set("n", "<leader>lt", "<cmd>ClangdSymbolInfo<cr>", opts)
  vim.keymap.set("n", "<leader>lm", "<cmd>ClangdMemoryUsage<cr>", opts)

  require("clangd_extensions.inlay_hints").setup_autocmd()
  require("clangd_extensions.inlay_hints").set_inlay_hints()
end

local status_ok, project_config = pcall(require, "rhel.clangd_wrl")
if status_ok then
  clangd_flags = vim.tbl_deep_extend("keep", project_config, clangd_flags)
end

local custom_on_init = function(client, bufnr)
  require("lvim.lsp").common_on_init(client, bufnr)
  require("clangd_extensions.config").setup {}
  require("clangd_extensions.ast").init()
  vim.cmd [[
  command ClangdToggleInlayHints lua require('clangd_extensions.inlay_hints').toggle_inlay_hints()
  command -range ClangdAST lua require('clangd_extensions.ast').display_ast(<line1>, <line2>)
  command ClangdTypeHierarchy lua require('clangd_extensions.type_hierarchy').show_hierarchy()
  command ClangdSymbolInfo lua require('clangd_extensions.symbol_info').show_symbol_info()
  command -nargs=? -complete=customlist,s:memuse_compl ClangdMemoryUsage lua require('clangd_extensions.memory_usage').show_memory_usage('<args>' == 'expand_preamble')
  ]]
end

local opts = {
  cmd = { provider, unpack(clangd_flags) },
  on_attach = custom_on_attach,
  on_init = custom_on_init,
}

require("lvim.lsp.manager").setup("clangd", opts)

-- install codelldb with :MasonInstall codelldb
-- configure nvim-dap (codelldb)
lvim.builtin.dap.on_config_done = function(dap)
  dap.adapters.codelldb = {
    type = "server",
    port = "${port}",
    executable = {
      -- provide the absolute path for `codelldb` command if not using the one installed using `mason.nvim`
      command = "codelldb",
      args = { "--port", "${port}" },

      -- On windows you may have to uncomment this:
      -- detached = false,
    },
  }

  dap.configurations.cpp = {
    {
      name = "Launch file",
      type = "codelldb",
      request = "launch",
      program = function()
        local path
        vim.ui.input({ prompt = "Path to executable: ", default = vim.loop.cwd() .. "/build/" }, function(input)
          path = input
        end)
        vim.cmd [[redraw]]
        return path
      end,
      cwd = "${workspaceFolder}",
      stopOnEntry = false,
    },
  }

  dap.configurations.c = dap.configurations.cpp
end

-- custom-keybinds
lvim.keys.visual_mode['p'] = "P"

-- Setup Lsp.
local capabilities = require("lvim.lsp").common_capabilities()
require("lvim.lsp.manager").setup("texlab", {
  on_attach = require("lvim.lsp").common_on_attach,
  on_init = require("lvim.lsp").common_on_init,
  capabilities = capabilities,
})

-- setup formatting
local formatters = require "lvim.lsp.null-ls.formatters"
formatters.setup { { name = "black", "latexindent" }, }

formatters.setup({
  { command = "black",       filetypes = { "py" } },
  { command = "latexindent", filetypes = { "python" } }
})

lvim.format_on_save.enabled = false
vim.diagnostic.config({ virtual_text = false })

-- setup linting
local linters = require "lvim.lsp.null-ls.linters"
linters.setup({
  { command = "flake8", filetypes = { "python" } },
  { command = "chktex", filetypes = { "tex" } },
})

-- setup debug adapter
lvim.builtin.dap.active = true
local mason_path = vim.fn.glob(vim.fn.stdpath "data" .. "/mason/")
pcall(function()
  require("dap-python").setup(mason_path .. "packages/debugpy/venv/bin/python")
end)


lvim.builtin.which_key.mappings["dm"] = { "<cmd>lua require('neotest').run.run()<cr>",
  "Test Method" }
lvim.builtin.which_key.mappings["dM"] = { "<cmd>lua require('neotest').run.run({strategy = 'dap'})<cr>",
  "Test Method DAP" }
lvim.builtin.which_key.mappings["df"] = {
  "<cmd>lua require('neotest').run.run({vim.fn.expand('%')})<cr>", "Test Class" }
lvim.builtin.which_key.mappings["dF"] = {
  "<cmd>lua require('neotest').run.run({vim.fn.expand('%'), strategy = 'dap'})<cr>", "Test Class DAP" }
lvim.builtin.which_key.mappings["dS"] = { "<cmd>lua require('neotest').summary.toggle()<cr>", "Test Summary" }


-- binding for switching
lvim.builtin.which_key.mappings["C"] = {
  name = "Python",
  c = { "<cmd>lua require('swenv.api').pick_venv()<cr>", "Choose Env" },
}

-- UltiSnip configuration.
vim.cmd([[
  let g:UltiSnipsExpandTrigger="<CR>"
  let g:UltiSnipsJumpForwardTrigger="<Plug>(ultisnips_jump_forward)"
  let g:UltiSnipsJumpBackwardTrigger="<Plug>(ultisnips_jump_backward)"
  let g:UltiSnipsListSnippets="<c-x><c-s>"
  let g:UltiSnipsRemoveSelectModeMappings=0
  let g:UltiSnipsEditSplit="tabdo"
  let g:UltiSnipsSnippetDirectories=[$HOME."/.config/nvim/UltiSnips"]
]])

-- Vimtex configuration.
vim.g.vimtex_view_method = "zathura"
vim.g.vimtex_quickfix_enabled = 0

-- Setup cmp.
vim.api.nvim_create_autocmd("FileType", {
  group = vim.api.nvim_create_augroup("LaTeXGroup", { clear = true }),
  pattern = "tex",
  callback = function()
    require("user.cmp")
  end,
})

-- Mappings
lvim.builtin.which_key.mappings["C"] = {
  name = "LaTeX",
  m = { "<cmd>VimtexContextMenu<CR>", "Open Context Menu" },
  u = { "<cmd>VimtexCountLetters<CR>", "Count Letters" },
  w = { "<cmd>VimtexCountWords<CR>", "Count Words" },
  d = { "<cmd>VimtexDocPackage<CR>", "Open Doc for package" },
  e = { "<cmd>VimtexErrors<CR>", "Look at the errors" },
  s = { "<cmd>VimtexStatus<CR>", "Look at the status" },
  a = { "<cmd>VimtexToggleMain<CR>", "Toggle Main" },
  v = { "<cmd>VimtexView<CR>", "View pdf" },
  i = { "<cmd>VimtexInfo<CR>", "Vimtex Info" },
  l = {
    name = "Clean",
    l = { "<cmd>VimtexClean<CR>", "Clean Project" },
    c = { "<cmd>VimtexClean<CR>", "Clean Cache" },
  },
  c = {
    name = "Compile",
    c = { "<cmd>VimtexCompile<CR>", "Compile Project" },
    o = {
      "<cmd>VimtexCompileOutput<CR>",
      "Compile Project and Show Output",
    },
    s = { "<cmd>VimtexCompileSS<CR>", "Compile project super fast" },
    e = { "<cmd>VimtexCompileSelected<CR>", "Compile Selected" },
  },
  r = {
    name = "Reload",
    r = { "<cmd>VimtexReload<CR>", "Reload" },
    s = { "<cmd>VimtexReloadState<CR>", "Reload State" },
  },
  o = {
    name = "Stop",
    p = { "<cmd>VimtexStop<CR>", "Stop" },
    a = { "<cmd>VimtexStopAll<CR>", "Stop All" },
  },
  t = {
    name = "TOC",
    o = { "<cmd>VimtexTocOpen<CR>", "Open TOC" },
    t = { "<cmd>VimtexTocToggle<CR>", "Toggle TOC" },
  },
}

-- install plugins
lvim.plugins = {
  "ChristianChiarulli/swenv.nvim",
  "stevearc/dressing.nvim",
  "mfussenegger/nvim-dap-python",
  "nvim-neotest/neotest",
  "nvim-neotest/neotest-python",
  "lervag/vimtex",
  "kdheepak/cmp-latex-symbols",
  "itspriddle/vim-shellcheck",
  "KeitaNakamura/tex-conceal.vim",
  "kovetskiy/sxhkd-vim",
  "SirVer/ultisnips",
  "waycrate/swhkd-vim",
  {
    "NvChad/nvim-colorizer.lua",
    config = function()
      require("colorizer").setup {
        filetypes = { "*" },
        user_default_options = {
          RGB = true,          -- #RGB hex codes
          RRGGBB = true,       -- #RRGGBB hex codes
          names = true,        -- "Name" codes like Blue or blue
          RRGGBBAA = true,     -- #RRGGBBAA hex codes
          AARRGGBB = true,     -- 0xAARRGGBB hex codes
          rgb_fn = true,       -- CSS rgb() and rgba() functions
          hsl_fn = true,       -- CSS hsl() and hsla() functions
          css = true,          -- Enable all CSS features: rgb_fn, hsl_fn, names, RGB, RRGGBB
          css_fn = true,       -- Enable all CSS *functions*: rgb_fn, hsl_fn
          -- Available modes for `mode`: foreground, background,  virtualtext
          mode = "background", -- Set the display mode.
          -- Available methods are false / true / "normal" / "lsp" / "both"
          -- True is same as normal
          tailwind = false,                                -- Enable tailwind colors
          -- parsers can contain values used in |user_default_options|
          sass = { enable = false, parsers = { "css" }, }, -- Enable sass colors
          virtualtext = "■",
          -- update color values even if buffer is not focused
          -- example use: cmp_menu, cmp_docs
          always_update = false
        },
        -- all the sub-options of filetypes apply to buftypes
        buftypes = {},
      }
    end,

  },
  {
    "catppuccin/nvim",
    name = "catppuccin",
    config = function()
      require("catppuccin").setup({
        flavour = "mocha",
        background = {
          light = "latte",
          dark = "mocha",
        },
        integrations = {
          cmp = true,
          gitsigns = true,
          nvimtree = true,
          telescope = true,
          notify = true,
          mini = true,
        },
        custom_highlights = function(colors)
          return {
            Comment = { fg = colors.lavendar },
            ["@constant.builtin"] = { fg = colors.peach, style = {} },
            ["@comment"] = { fg = colors.surface2, style = { "italic" } },
          }
        end
      })
    end,
  },
}

vim.opt.guifont = "monospace:h17" -- the font used in graphical neovim applications
vim.opt.shiftwidth = 2            -- the number of spaces inserted for each indentation
vim.opt.tabstop = 2               -- insert 2 spaces for a tab
vim.opt.relativenumber = false    -- relative line numbers
vim.opt.wrap = true               -- wrap lines
