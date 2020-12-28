# paperless-exporter

Export from Mariner Paperless app to just files with tags.

This is just a personal project to move my documents out of [Paperless](https://marinersoftware.com/product/paperless/) and into just files with proper names, tags and comments, using only MacOS features to store the same metadata.

Unfortunately Paperless doesn't have an export functionality, which essentially vendor-locks you.

## Instructions/Assumptions
Not sure if this utility will be useful to anyone else, but it works on the following assumptions:

- Your library is NOT encrypted. If it is encrypted you need to remove the encryption with your password through the app first.
- You run this from the main library directory. To get there you need to:

    - find your library (probably called "Paperless Library")
    - right click it
    - select "Show Package Contents"

I thoroughly recommend making a backup/copy of you library before you mess with it in any way.

## Limitations
There are probably other limitations in this utility. This exports only the document "name" (aka Merchant), category, subcategory, notes and tags.

Category and subcategory are treated the same as tags, and are added as MacOS tags.

Notes are added as MacOS file comments.

Pull requests are of course welcome.

## Final Disclaimer
Feel free to use or improve this, but you do so at your own risk. I'm not responsible for any data loss or other issues caused by the use of this code and I am in no way affiliated with Mariner Software/Paperless.