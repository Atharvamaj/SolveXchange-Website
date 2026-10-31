# SolveXchange Website

<p align="center"><img src="images/logo.webp" width="100" alt="SolveXchange logo"></p>

**Turning Vision into Reality, One Pitch at a Time.**

[Visit the website](https://www.solvexchange.org)

SolveXchange is a student led initiative helping young people turn ideas for their communities into real projects. This repository contains its public website, made with HTML, CSS and JavaScript and ready for GitHub Pages.

## Why this fork exists

This project is forked from [yih0nk/SolveXchange-Website](https://github.com/yih0nk/SolveXchange-Website). The original project used Python and Flask. This fork keeps the public website separate from the SolveXLabs PWA and makes it possible to host the website on GitHub Pages without a backend or database.

The original project and its contributors are credited for the website, content and visual identity. The original layout, colors, typography and carousel are retained. This fork removes the backend and applies the requested content, sizing and alignment fixes.

## Run it

Open the folder with a static web server. For example, if Python is installed:

```sh
python -m http.server 8000
```

Then open http://localhost:8000. Python is only used for this optional local preview. The published website does not run Python.

There is no package installation or build step.

## Edit it

| Page | File |
| --- | --- |
| Home | `index.html` |
| About Us | `html/aboutus.html` |
| Resources | `html/resources.html` |
| FAQ | `html/faq.html` |
| Get Involved | `html/getinvolved.html` |

Images are in `images`. Page styles are in `css`. The small layout fixes are in `css/adjustments.css`. Navigation and expandable sections are in `javascript/site.js`. The original carousel animation is in `css/index.css`, with its loop fixes in `css/adjustments.css`. The script waits for its pictures to load before scrolling.

The success stories keep the original automatic scrolling carousel. The loop spacing is corrected and the images scale with the screen. Hovering or focusing the strip pauses it. Reduced motion settings stop the animation.

If you add or remove a page, update the navigation in the five HTML files. Keep only the images that the pages use.

## Publish on GitHub Pages

1. Replace the old website files with this folder's contents, keeping the same folder structure. Keep your existing `.git` folder so the repository history stays intact. Review the changes, then commit and push them yourself to your chosen branch.
2. In repository Settings, open Pages.
3. Choose Deploy from a branch, then your branch and the root folder.
4. Set the custom domain to `www.solvexchange.org` and configure its DNS using the instructions GitHub provides.
5. Enable HTTPS when it becomes available.

Include `.nojekyll` and `CNAME` when uploading. The separate PWA subdomain should keep its existing DNS settings.

The old Flask application, database, virtual environment, login pages and forum are not part of this version. External registration forms, lesson links and social links still open their existing services.

## Folder structure

The root index.html is the home page. Named pages live in html, styles in css, scripts in javascript and pictures in images. The root 404.html and Google verification file must stay at the root for hosting and verification.

## Before going live

Keep the existing site online while testing this copy on the GitHub Pages preview address. Do not configure the production custom domain or change DNS until the preview is ready. CNAME contains the intended production domain; leave it out of the staging upload to use the github.io address.

When ready, configure www.solvexchange.org under repository Settings > Pages, update only its website DNS records, and enable HTTPS. Preserve email MX records, Google verification TXT records and the separate SolveXLabs subdomain. Once the replacement works at www.solvexchange.org with HTTPS, retire the original website backend. Keep a backup of its source. The separate SolveXLabs PWA must remain running.

The named files change page URLs. Configure permanent HTTP 301 redirects at your proxy or redirect capable host from /aboutus and /aboutus/ to /html/aboutus.html, and likewise for resources, faq and getinvolved. GitHub Pages does not provide configurable server redirect rules. The included 404 script helps visitors following old links but returns an initial 404 and is not a substitute for SEO redirects.

Keep googlea5f25ffb4bd4c8ed.html at the domain root. It verifies ownership, not individual pages, so do not create extra tokens for each page. Submit https://www.solvexchange.org/sitemap.xml in Google Search Console after launch. robots.txt points to that sitemap; each public page also has a canonical URL. No Change of Address request is needed when retaining the same domain.

If you use the production sitemap and canonical URLs on a preview, keep the preview temporary and unlinked. Add a noindex meta tag to staging pages only if you want to exclude the preview from search, and remove it before production.

Bug reports go to solvexchange.dev@gmail.com.

The primary website address is https://www.solvexchange.org. Configure the apex domain solvexchange.org to redirect to this www address. The old website will no longer be used once the replacement is live; redirects preserve old links without keeping the old application running.
