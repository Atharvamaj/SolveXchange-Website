# SolveXchange

<p align="center"><img src="images/logo.webp" width="100" alt="SolveXchange logo"></p>

[www.solvexchange.org](https://www.solvexchange.org)

The public website for SolveXchange. Built with HTML, CSS and JavaScript.

## Why I forked it

The original site used Flask, but the public website doesn't need a backend anymore. I made this fork to move it to GitHub Pages and make it easier to work on.

I wanted to keep the original look and content while fixing the spacing, image alignment and mobile layout. The login and forum pages have been removed. SolveXLabs is a separate app and still has its own backend.

The original website is from [yih0nk/SolveXchange-Website](https://github.com/yih0nk/SolveXchange-Website). Credit to the original contributors for the design and content.

## Where everything is

| File or folder | What's in it |
| --- | --- |
| `index.html` | Home page |
| `html/` | About Us, Resources, FAQ and Get Involved |
| `css/` | Styles and layout fixes |
| `javascript/` | Menu, expandable sections and other interactions |
| `images/` | Website images and logos |
| `404.html` | Missing page and fallback for old page links |
| `CNAME` | The website domain |
| `sitemap.xml` | Public page URLs for search engines |
| `robots.txt` | Crawler instructions and sitemap location |

## Making changes

Edit the page in `html/`, or `index.html` for the home page. Keep styles in `css/`, scripts in `javascript/` and images in `images/`.

Most pages use `css/adjustments.css` for layout fixes. Get Involved uses `css/getinvolved-adjustments.css`. Shared responsive fixes are in `css/responsive.css`, and the menu and expandable sections are in `javascript/site.js`.

Check both desktop and mobile after changing a layout. Let boxes grow with their text instead of giving them a fixed height that cuts things off.

If you add a page, update the navigation and `sitemap.xml` too.

## Hosting

This version is set up for GitHub Pages. Put the website files at the repository root and select the branch you want to publish under Settings > Pages.

The custom domain is `www.solvexchange.org`. Keep `CNAME` and `.nojekyll` in the root. The CNAME file should contain only:

```text
www.solvexchange.org
```

The old website can be shut down once this version works on the domain with HTTPS. Keep a backup first. Don't shut down SolveXLabs or change its subdomain or the email records.

Changing CNAME in this folder doesn't change DNS. The domain's website DNS records still need to point to the new host. The address without www should redirect to the www address.

## Old links and Google

The page addresses have changed. For example, `/aboutus/` is now `/html/aboutus.html`.

The 404 script helps visitors reach the new pages, but it isn't a proper server redirect. Permanent 301 redirects still need to be configured at a host or proxy that supports them. GitHub Pages doesn't have a setting for custom server redirect rules.

Keep `googlea5f25ffb4bd4c8ed.html` in the root. It's the existing Google verification file. After launch, submit `https://www.solvexchange.org/sitemap.xml` in Google Search Console.

## Found a bug?

Email [solvexchange.dev@gmail.com](mailto:solvexchange.dev@gmail.com) with the page link and what went wrong. A screenshot and your screen size help too.
