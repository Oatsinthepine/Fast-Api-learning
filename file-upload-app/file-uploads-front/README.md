# React + TypeScript + Vite

This is a simple file upload application built with React, TypeScript, and Vite. 


## Note on restructure project structure for front-end (Vite + npm):

- what I have done is when restructuring, I move the entire `file-uploads-front` directory into `file-upload-app`, which can cause issues with the Vite development server and its cache error. Unable to `npm run dev` after moving the directory.

### Solution to fix the Vite cache error regarding the directory move:

The error of seeing is a Vite/node_modules cache issue that’s very common after moving directories, especially with a heavy front-end toolchain like Vite + npm. 
Node’s module resolution is very dependent on filesystem paths, and cached builds (including Vite, Webpack, etc.) can break if those paths change.

How to Fix Vite/NPM Errors After Moving a Project Directory

** The safest solution is always: Move entire directory to the target directory first! then Delete and Reinstall **:
	1.	Delete the existing `node_modules` and `package-lock.json` files
	2.	Reinstall your dependencies

### Steps:

1. Delete the existing `node_modules` and `package-lock.json` files, make sure you are in the `file-uploads-front` directory:
   ```bash
   cd file-upload-app/file-uploads-front
   rm -rf node_modules package-lock.json
   ```
2. Reinstall your dependencies:
    ```bash
    npm install
    ```
   
Why did this happen?

	•	node_modules contains a lot of absolute and relative paths cached from the previous directory location.
	•	Moving the entire folder invalidates these paths, causing errors when npm/node tries to resolve packages.
	•	Removing and reinstalling ensures everything is rebuilt for the new path.

⸻

## General Tip for Any Moved JS Project

Whenever you move a Node.js (npm/yarn/pnpm) project:

	•	Always delete node_modules and lock files, then reinstall.
	•	If you see strange “path not exported” or module resolution errors, this is almost always the fix.