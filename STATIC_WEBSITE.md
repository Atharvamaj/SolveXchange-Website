# SolveXchange static website

This conversion uses `Atharvamaj/SolveXchange-Website`, branch `master`, commit `0715eb8`, verified against the latest master branch during conversion. The live website could not be reached during conversion, so deployment parity with its server is unverified.

## Run or download

The ready-to-host ZIP contains the complete static website: HTML, CSS, JavaScript, images, fonts and public PDFs. No Flask, database, mail server, Node installation or build step is needed to host these exported files.

To regenerate from this repository, install Python 3.10 or later and run:

```sh
python scripts/build_static.py
python -m http.server 8000 --directory dist
```

Visit http://localhost:8000. The exporter uses only Python's standard library and checks all local HTML links/assets and JavaScript for backend calls. Edit the files in `templates/` and `static/`, then regenerate. The exporter supports the existing public templates' simple inheritance, named blocks and `url_for('static', filename=...)` expressions; it is not a general Jinja renderer.

## GitHub Pages

1. Merge the static conversion into `master`. In repository **Settings → Pages**, select **GitHub Actions** as the build source.
2. Run **Deploy static website to GitHub Pages** from **Actions**, choosing the `master` branch. Later pushes to `master` trigger deployment automatically.
3. Set the Pages custom domain to `solvexchange.org`. The exported `CNAME` already contains this domain. Configure the domain's apex/www DNS using the values GitHub Pages displays and enable HTTPS when available.
4. If you later merge into another production branch, update `branches` in `.github/workflows/pages.yml` to that one branch.

Alternatively, put the ZIP's contents at the root of a dedicated Pages repository and publish that branch's root. The included `.nojekyll` prevents Jekyll processing. Relative page and asset links also support a GitHub project subpath. Clean paths such as `/aboutus/` and flat aliases such as `/aboutus.html` are included.

Only the generated `dist/` directory is deployed by the workflow. The legacy Flask files, virtual environment, database and mail/account logic remain outside the published artifact. Do not upload the entire original repository as the static website.

## What changed

- Preserved the public Home, About Us, Resources, FAQ and Get Involved page designs, images, external forms, social links, sponsorship materials, FAQ expanders, mobile menu and CSS carousel.
- Converted Flask inheritance and asset helpers into ordinary HTML and relative URLs.
- Replaced the database forum with a Community page linking to the existing Google Classroom, Instagram and team email. Website posts, replies, likes and accounts are no longer provided. No database content has been exported.
- Old `/forum`, `/login` and `/register` links open the community information; there is no simulated login or local-only forum.
- Removed unused jQuery and excluded account/forum scripts from the public output. Google Fonts, linked Google Forms/Classroom and social platforms still require internet access and remain external services.
- Included a custom 404 page and existing Google site verification file.

The separate SolveXLabs PWA and its backend are outside this conversion. When switching apex/www DNS, retain the PWA subdomain records. This work does not change DNS, stop services or migrate PWA accounts/data.

## Responsive layout and image updates

Responsive content widths and spacing now support phones, tablets and desktops. The update restores homepage sections previously hidden on mobile, fixes stretched images and the squeezed judge biography, and makes success stories swipeable on phones. Values descriptions remain visible on touchscreens. Menus and expansion controls support keyboard input and larger touch targets.

WebP assets are committed under `static/images/optimized/`; normal builds still require only Python's standard library. The optional `python scripts/optimize_images.py` regeneration command requires Pillow. Slides and logos use lossless compression; other images use quality 86 with a 1400-pixel maximum dimension. Original source images remain in the repository. Lazy loading, original image size settings and consolidated font requests improve mobile loading.

Validation compares all exported body text with the previous static version, checks local links/assets and examines layouts at small-phone, phone, tablet and desktop widths. No deployment or DNS change is included.

## Original design corrections

Desktop pages now use the original master typography, button styling and image crops. The responsive presentation rules apply to phones and tablets. Targeted desktop rules align the values cards, participation cards, footer columns and FAQ actions, while keeping the judge biography readable. The export preserves width and height attributes from the original HTML instead of replacing them. Font imports are removed as complete CSS statements so page font rules remain valid.

Checked the original image size attributes on all six public pages, unchanged body text on all 19 exports, and page overflow at four screen widths.
