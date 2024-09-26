;;; debug-template.el --- Description -*- lexical-binding: t; -*-
;;
;; Copyright (C) 2024 Andreas Ratchev
;;
;; Author: Andreas Ratchev <andy@Chomsky>
;; Maintainer: Andreas Ratchev <andy@Chomsky>
;; Created: September 02, 2024
;; Modified: September 02, 2024
;; Version: 0.0.1
;; Keywords: abbrev bib c calendar comm convenience data docs emulations extensions faces files frames games hardware help hypermedia i18n internal languages lisp local maint mail matching mouse multimedia news outlines processes terminals tex tools unix vc wp
;; Homepage: https://github.com/andy/debug-template
;; Package-Requires: ((emacs "24.3"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;;  Description
;;
;;; Code:



(provide 'debug-template)
(dap-register-debug-template
  "Python :: Run file from project directory (return fibonacci)"
  (list :name "Python :: Run file from project directory (Custom)"
        :type "python"
        :args "examples/return-fibonacci.lox"
        :cwd "${workspaceFolder}"
        ;; :env '(("PYTHONPATH" . "/home/andy/Projects/Python/crafting-interpreters"))
        :module nil
        :program "plox.py"
        :request "launch"))
;;; debug-template.el ends here
