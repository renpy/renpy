(defun renpy-mode () 
  (interactive)
  (python-mode) 
  (setq font-lock-keywords 
        (append '( ("\\b\\(menu\\|call\\|\\$\\|python\\|image\\|scene\\|show\\|hide\\|init\\|set\\|jump\\|at\\|with\\)\\b" (0 font-lock-keyword-face)) 
                   ("\\b\\(label\\|menu\\)\\s-+\\(\\w+\\):" (1 font-lock-keyword-face) (2 font-lock-function-name-face))
                  ) python-font-lock-keywords)) 
  (font-lock-mode 1) 
  (font-lock-fontify-buffer))
