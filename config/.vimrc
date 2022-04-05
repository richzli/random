" Code collapsing
set foldmethod=syntax
highlight Folded ctermbg=000

" display line numbers on the sidebar
set number
set relativenumber

augroup numbertoggle
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
  autocmd BufLeave,FocusLost,InsertEnter   * set norelativenumber
augroup END

" Display current line and column on the bottom bar
set ruler

" Set tabs to be 4 spaces wide, except in c files
set tabstop=4
set softtabstop=4
set shiftwidth=4
autocmd FileType c setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab

" Automatically indent code when going to the next line
set autoindent

" Expand tab characters to be spaces.
set expandtab

" highlight search results
set hlsearch

" start search without having to submit
set incsearch

" allow mouse for pasting etc
set mouse=a

"Keep 7 lines visible at the top and bottom of the screen when scrolling
set so=7

" use n and N to center the next search result on the screen
nmap n nzz
nmap N Nzz

" show whitespace
set list
set listchars=tab:>.,trail:.

" Flash on the screen instead of making the bell sound
set noerrorbells
set visualbell

filetype on
syntax on
