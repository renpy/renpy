; (X)Emacs mode. Requires python-mode to be installed to work.
; 
; To use, M-x load-file renpy-mode.el RET M-x renpy-mode RET

(require 'python-mode)

; How we highlight a single keyword.
(defun renpy-keyword (kw)
  (list
   (concat "\\b" kw "\\b")
   '( 0 font-lock-keyword-face)
   )
  )

; The big list of things we highlight.
(setq renpy-font-lock-keywords
      (list       
       (renpy-keyword "at")
       (renpy-keyword "call")
       (renpy-keyword "hide")
       (renpy-keyword "if")
       (renpy-keyword "image")
       (renpy-keyword "init")
       (renpy-keyword "jump")
       (renpy-keyword "menu")
       (renpy-keyword "python")
       (renpy-keyword "return")
       (renpy-keyword "scene")
       (renpy-keyword "set")
       (renpy-keyword "show")
       (renpy-keyword "with")
       (renpy-keyword "while")
       
       ; Python keywords we want to keep highlighting.

       (renpy-keyword "and")
       (renpy-keyword "assert")
       (renpy-keyword "break")
       (renpy-keyword "class")
       (renpy-keyword "continue")
       (renpy-keyword "def")
       (renpy-keyword "del")
       (renpy-keyword "elif")
       (renpy-keyword "else")
       (renpy-keyword "except")
       (renpy-keyword "exec")
       (renpy-keyword "finally")
       (renpy-keyword "for")
       (renpy-keyword "from")
       (renpy-keyword "global")
       (renpy-keyword "import")
       (renpy-keyword "in")
       (renpy-keyword "is")
       (renpy-keyword "lambda")
       (renpy-keyword "not")
       (renpy-keyword "or")
       (renpy-keyword "pass")
       (renpy-keyword "print")
       (renpy-keyword "raise")
       (renpy-keyword "try")
       (renpy-keyword "yield")
       
       '("\\$" (0 font-lock-keyword-face) )

       '("\\b\\(label\\|menu\\)\\s-+\\(\\w+\\):" (1 font-lock-keyword-face) (2 font-lock-function-name-face))
       '("\\b\\(def\\|class\\)\\s-+\\(\\w+\\)" (1 font-lock-keyword-face) (2 font-lock-function-name-face))
       ))

(defun renpy-mode () 
  (interactive)
  (python-mode) 
  
; (setq font-lock-keywords 
  ;      (append '( ("\\b\\(menu\\|call\\|\\$\\|python\\|image\\|scene\\|show\\|hide\\|init\\|set\\|jump\\|at\\|with\\)\\b" (0 font-lock-keyword-face)) 
  ;                 ("\\b\\(label\\|menu\\)\\s-+\\(\\w+\\):" (1 font-lock-keyword-face) (2 font-lock-function-name-face))
  ;                ) python-font-lock-keywords)) 
  

  (setq font-lock-keywords renpy-font-lock-keywords)

  (font-lock-mode 1) 
  (font-lock-fontify-buffer)
  (auto-fill-mode 1)
  (setq indent-line-function 'renpy-indent-line)
  (setq fill-paragraph-function 'renpy-fill-paragraph)
  )

; Computes the start of the current string.
(defun renpy-string-start ()
  (nth 8 (parse-partial-sexp (point-min) (point)))
  )

; Computes the amount of indentation needed to put the current string
; in the right spot.
(defun renpy-string-indentation () 
  (+ 1
     (save-excursion
       (- (goto-char (renpy-string-start))
          (progn (beginning-of-line) (point)))
       )
     )
  )

; Figures out the prefix, without the line indentation, required to 
; get strings to line up right after a fill.
(defun renpy-string-fill-prefix () 
  (make-string 
   (- (renpy-string-indentation)
      0
;      (save-excursion
;        (goto-char (renpy-string-start))
;        (current-indentation)
;        )
      ) ?\  )
  )


; Indents a paragraph. We also handle strings properly.
(defun renpy-fill-paragraph (&optional justify)
  (interactive)
  (if (eq (py-in-literal) 'string)
      (let* ((string-indentation (renpy-string-indentation))
             (fill-prefix (renpy-string-fill-prefix))
             (fill-column (- fill-column string-indentation))
             (fill-paragraph-function nil)
             (indent-line-function nil)
             )
        
        ; Fixup the fill.
        ;(save-excursion
        ;  (goto-char (+ 1 (nth 8 (parse-partial-sexp (point-min) (point)))))
        ;  (insert (make-string (renpy-string-indentation) ?\ ))
        ;  )

        (message "fill prefix: %S" fill-prefix)
        ; (py-fill-paragraph justify)

        (py-fill-string (renpy-string-start))

        ;(save-excursion
        ;  (goto-char (+ 1 (nth 8 (parse-partial-sexp (point-min) (point)))))
        ;  (delete-char (renpy-string-indentation))
        ;  )
        
        t
        )
    (py-fill-paragraph justify)
    )   
  )

; Indents the current line. 
(defun renpy-indent-line (&optional arg)
  (interactive)

  ; Let python-mode indent. (Always needed to keep python-mode sane.)
  (py-indent-line)

  ; Reindent strings if appropriate.
  (save-excursion
    (beginning-of-line)
    (if (eq (py-in-literal) 'string)
        (progn 
          (delete-horizontal-space)
          (indent-to (renpy-string-indentation))
          )
      ))

  (if ( < (current-column) (current-indentation) )
      (back-to-indentation) )

  )
