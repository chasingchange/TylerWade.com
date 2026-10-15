# Add photos to the gallery

Drop photos in this folder and they appear at the top of the gallery on the site.

1. On GitHub, open this `add-to-gallery` folder on the `main` branch.
2. Click **Add file → Upload files** and drag your photos in (JPG, PNG, WebP, or iPhone HEIC).
3. Click **Commit changes**.

About a minute later a GitHub Action resizes each photo, makes its thumbnail,
adds it to `gallery.json`, and empties this folder again. You can watch it run
under the repository's **Actions** tab.

Upload the full-size originals: the Action shrinks them for the web, so a
bigger file means a sharper photo when someone clicks to view it.

To remove a photo later, delete its line from `gallery.json`.
