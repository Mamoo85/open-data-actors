# Open Data Actors: all actors by use case

Every public Apify actor from [transparent_meteorite](https://apify.com/transparent_meteorite), grouped by the job it does. All are pay per result with no monthly rental; prices are the main result event on the Apify Free plan (paid Apify plans pay less on actors with tiered pricing). Each actor's Pricing tab on Apify is the final word.

Generated from the same map that writes the "Related actors" section in every actor README (`apify_crosslink.py`).

## Common stacks

- **Account research:** [Company Enrichment by Domain](https://apify.com/transparent_meteorite/company-enrichment-by-domain) + [Website Email Extractor](https://apify.com/transparent_meteorite/website-contact-extractor) + [Tech Stack Detector](https://apify.com/transparent_meteorite/website-tech-stack-detector), about **$9.00** per 1,000 company domains at Free-plan prices ($5.50 once the scheduled price changes from Oct 30, 2026 apply).
- **Local lead list with contacts:** [Local Business Leads](https://apify.com/transparent_meteorite/local-business-leads) + [Website Email Extractor](https://apify.com/transparent_meteorite/website-contact-extractor), about **$5.00** per 1,000 places at most (contact pass only runs on places that list a website) at Free-plan prices ($3.90 once the scheduled price changes from Oct 30, 2026 apply).
- **Web-design prospecting:** [Web Design Leads](https://apify.com/transparent_meteorite/website-redesign-leads) + [Website Email Extractor](https://apify.com/transparent_meteorite/website-contact-extractor) + [Technical SEO Audit](https://apify.com/transparent_meteorite/technical-seo-page-audit), about **$9.00** per 1,000 leads, one audited page each at Free-plan prices ($7.90 once the scheduled price changes from Oct 30, 2026 apply).

## Company and account research

Turn a list of domains or company names into firmographics, contacts and technology data.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Company Enrichment by Domain: LinkedIn, Emails, Tech Stack](https://apify.com/transparent_meteorite/company-enrichment-by-domain) | domain in, company row out: name, logo, LinkedIn URL, role emails, email provider, tech stack | $5.00 (from Oct 30, 2026: $1.50) |
| [Website Email Extractor: Contacts, Phones, Socials](https://apify.com/transparent_meteorite/website-contact-extractor) | emails, phones and social profiles from each website, with the page each was found on | $2.00 |
| [Tech Stack Detector: Website Technology Lookup & Monitor](https://apify.com/transparent_meteorite/website-tech-stack-detector) | CMS, ecommerce platform, analytics, CDN and hosting behind each website | $2.00 |
| [WHOIS & Domain Lookup: RDAP, DNS, Subdomains, SSL](https://apify.com/transparent_meteorite/domain-intelligence-lookup) | WHOIS/RDAP dates, DNS, SPF/DMARC and subdomains for a list of domains | $2.00 |
| [Shopify Store Leads Scraper: Apps, Theme, Contacts](https://apify.com/transparent_meteorite/shopify-store-leads) | Shopify stores with detected apps, theme, product count and contacts | $4.00 |
| [Facebook Pages Scraper: Contacts, Followers, Ad Status](https://apify.com/transparent_meteorite/facebook-pages-scraper) | public Facebook Pages: category, followers, contact details | $3.00 |

## Local business leads

Find and qualify local businesses by category and place.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Local Business Leads: No-Website Finder (OpenStreetMap)](https://apify.com/transparent_meteorite/local-business-leads) | local businesses from OpenStreetMap by type and place, including ones with no website | $3.00 (from Oct 30, 2026: $1.90) |
| [Web Design Leads: Local Businesses With No or Weak Websites](https://apify.com/transparent_meteorite/website-redesign-leads) | local businesses with no website or a weak one, with the reasons | $4.00 |
| [Google Maps Listing Change Monitor: Ratings, Hours, Closures](https://apify.com/transparent_meteorite/maps-listing-change-monitor) | alerts when a Google Maps listing closes, reopens or drops in rating | $3.00 |
| [Website Email Extractor: Contacts, Phones, Socials](https://apify.com/transparent_meteorite/website-contact-extractor) | emails, phones and social profiles from each website, with the page each was found on | $2.00 |

## Buying signals from public records

New registrations, filings and permits from official government open data, usually updated daily.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [FMCSA New Motor Carrier Leads: New Authority, Email & Phone](https://apify.com/transparent_meteorite/fmcsa-new-carrier-leads) | new US trucking companies (USDOT/MC) with the email and phone from their FMCSA filing | $8.00 (from Nov 5, 2026: $2.40) |
| [SEC Form D Scraper: Startup Funding Leads from EDGAR](https://apify.com/transparent_meteorite/sec-form-d-funding-leads) | recently funded companies from new SEC Form D filings | $2.50 (from Oct 30, 2026: $1.90) |
| [Business Entity Search: 6-State SOS Registry Lookup](https://apify.com/transparent_meteorite/business-entity-search) | look up companies in 6 state Secretary of State registries (KYB) | $2.00 |
| [Building Permits Leads: US City Permits & Violations](https://apify.com/transparent_meteorite/building-permits-leads) | building permits from 9 city and county open-data portals | $1.50 |
| [Contractor License Lookup: Multi-State Official Data](https://apify.com/transparent_meteorite/contractor-license-lookup) | verify contractor and trade licenses from 6 states' open data | $2.00 |
| [New Liquor License Applications by State: NY, TX, MO](https://apify.com/transparent_meteorite/state-liquor-license-new-applications) | new liquor license applications from NY, TX and MO open data | $4.00 |
| [City Council Meetings & Agendas: Legistar Votes, PDFs](https://apify.com/transparent_meteorite/city-council-agendas) | council meetings, agenda items and votes from 18 US cities (Legistar) | $1.00 (from Oct 30, 2026: $0.49) |
| [Open Payments Scraper: CMS Pharma Payments to Doctors](https://apify.com/transparent_meteorite/medicare-open-payments-doctors) | CMS Open Payments from drug and device makers to doctors | $6.00 |

## Hiring and job-market data

Open roles straight from company career sites, plus signals computed from them.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Greenhouse & Lever Jobs Scraper: Career Site Jobs](https://apify.com/transparent_meteorite/ats-open-roles) | open roles from Greenhouse, Lever, Ashby, Workable, SmartRecruiters and Recruitee boards | $2.00 |
| [Workday Jobs Scraper: Salary, Remote & Level Filters](https://apify.com/transparent_meteorite/workday-jobs-scraper) | jobs from any myworkdayjobs.com career site, with salary, remote and level filters | $1.00 (from Oct 30, 2026: $2.00) |
| [Hiring Velocity Signals: Company Growth from Job Posts](https://apify.com/transparent_meteorite/hiring-velocity-signals) | one row per company: open roles, new roles in 7/30 days, hiring trend | $4.00 |
| [Salary Benchmarks from Job Posts: Pay Ranges by Role](https://apify.com/transparent_meteorite/salary-transparency-index) | pay-range percentiles by role and location from pay-transparent job posts | $5.00 |
| [Visa Sponsorship Jobs Scraper: Greenhouse, Lever, Ashby](https://apify.com/transparent_meteorite/visa-sponsorship-jobs-scraper) | jobs whose posting mentions visa sponsorship (Greenhouse, Lever, Ashby) | $2.50 |
| [WARN Layoff Notices Scraper: 8 States + New-Only Alerts](https://apify.com/transparent_meteorite/warn-layoff-alerts) | WARN Act layoff and closure notices from 8 state sources in one schema | $3.00 (from Oct 30, 2026: $1.00) |

## Government contracts and compliance

Federal opportunities, awards and sanctions screening from official sources.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [SAM.gov Opportunities Scraper: Federal Government Contracts](https://apify.com/transparent_meteorite/sam-gov-opportunities) | SAM.gov federal contract opportunities and award notices | $2.50 |
| [Federal Grants & Contracts Finder: Grants.gov + USAspending](https://apify.com/transparent_meteorite/federal-grants-contracts) | Grants.gov opportunities and USAspending awards in one schema | $2.00 |
| [OFAC Sanctions Screening: SDN, EU, UN & UK, Fuzzy Match](https://apify.com/transparent_meteorite/sanctions-screening) | fuzzy-match names against OFAC, UN, EU and UK sanctions lists | $4.00 (from Oct 30, 2026: $3.00) |

## Company monitoring

Watch companies for news, layoffs and developer activity.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Company News Monitor: Brand & Keyword News Alerts](https://apify.com/transparent_meteorite/company-news-monitor) | news about companies and keywords from 75 publisher RSS feeds, new articles only | $2.00 |
| [WARN Layoff Notices Scraper: 8 States + New-Only Alerts](https://apify.com/transparent_meteorite/warn-layoff-alerts) | WARN Act layoff and closure notices from 8 state sources in one schema | $3.00 (from Oct 30, 2026: $1.00) |
| [Hacker News Scraper: npm & PyPI Developer Signals](https://apify.com/transparent_meteorite/developer-signals) | Hacker News mentions plus npm and PyPI versions and downloads | $1.00 (from Oct 30, 2026: $2.00) |
| [PyPI Package Stats and New Releases Tracker](https://apify.com/transparent_meteorite/pypi-package-stats-releases) | PyPI package releases, cadence and download counts | $2.00 |

## SEO and website audits

Crawl, audit and map websites and search results.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Technical SEO Audit: Site Crawler with 0-100 Score](https://apify.com/transparent_meteorite/technical-seo-page-audit) | 0-100 technical SEO score, top issues and broken links per page or whole site | $3.00 (from Oct 30, 2026: $1.90) |
| [Sitemap Extractor & Broken Link Checker: All URLs](https://apify.com/transparent_meteorite/sitemap-link-inventory) | every URL in a site's sitemaps, with optional status check | $1.00 (from Oct 30, 2026: $0.50) |
| [Google Search Results Scraper: SERP to JSON, Real URLs](https://apify.com/transparent_meteorite/google-search-results-scraper) | Google results pages as JSON with real target URLs | $4.50 |
| [Google Trends Scraper: Compare, Related, Trending Now](https://apify.com/transparent_meteorite/google-trends-scraper) | Google Trends interest over time, by region and related queries | $1.50 |
| [SSL Certificate Subdomain Finder: CT Log Search](https://apify.com/transparent_meteorite/ssl-certificate-subdomain-finder) | subdomains of a domain from Certificate Transparency logs | $3.00 |
| [WHOIS & Domain Lookup: RDAP, DNS, Subdomains, SSL](https://apify.com/transparent_meteorite/domain-intelligence-lookup) | WHOIS/RDAP dates, DNS, SPF/DMARC and subdomains for a list of domains | $2.00 |
| [Tech Stack Detector: Website Technology Lookup & Monitor](https://apify.com/transparent_meteorite/website-tech-stack-detector) | CMS, ecommerce platform, analytics, CDN and hosting behind each website | $2.00 |

## Ecommerce and app research

Product, ranking and review data for marketplaces and app stores.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Amazon Product Search: prices, ratings, ASINs](https://apify.com/transparent_meteorite/amazon-product-search) | Amazon products by keyword, URL or ASIN: price, rating, reviews | $4.00 |
| [Amazon Best Sellers Scraper: Top 100 Ranks, 21 Countries](https://apify.com/transparent_meteorite/amazon-bestsellers) | Amazon Best Sellers and New Releases ranks in 21 countries | $1.90 |
| [Shopify Store Leads Scraper: Apps, Theme, Contacts](https://apify.com/transparent_meteorite/shopify-store-leads) | Shopify stores with detected apps, theme, product count and contacts | $4.00 |
| [App Store Reviews Scraper: iOS Ratings, 150+ Countries](https://apify.com/transparent_meteorite/app-store-reviews) | Apple App Store reviews and ratings for any iOS app, 150+ countries | $0.50 (from Oct 30, 2026: $0.30) |

## Ads and creator marketing

Competitor ads and creator sponsorships.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [Meta Ad Library Scraper: Facebook Ad Library & Instagram Ads](https://apify.com/transparent_meteorite/meta-ad-library) | ads from the public Meta Ad Library by keyword or Page | $0.65 (from Oct 30, 2026: $0.57) |
| [YouTube Sponsorship Tracker: Brand Deals, Promo Codes](https://apify.com/transparent_meteorite/youtube-sponsorship-tracker) | which YouTubers a brand sponsors, with promo codes and links | $2.00 |
| [Facebook Pages Scraper: Contacts, Followers, Ad Status](https://apify.com/transparent_meteorite/facebook-pages-scraper) | public Facebook Pages: category, followers, contact details | $3.00 |

## YouTube data

Videos, channels, comments, Shorts and transcripts from public YouTube pages.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [YouTube Video Scraper: Search, Channels, Playlists](https://apify.com/transparent_meteorite/youtube-video-scraper) | YouTube videos from searches, channels or playlists with views and dates | $2.00 |
| [YouTube Channel Scraper: Subscribers, About, Videos](https://apify.com/transparent_meteorite/youtube-channel-scraper) | YouTube channel stats, about info and latest videos | $0.80 |
| [YouTube Comments Scraper: Comments & Replies Export](https://apify.com/transparent_meteorite/youtube-comments-scraper) | public YouTube comments and replies | $1.00 |
| [YouTube Shorts Scraper: Views, Likes, Comments](https://apify.com/transparent_meteorite/youtube-shorts-scraper) | YouTube Shorts with views, likes and publish dates | $2.00 |
| [YouTube Transcript Extractor: Text, SRT, VTT](https://apify.com/transparent_meteorite/youtube-transcript-extractor) | YouTube transcripts as text, SRT or VTT | $3.00 |
| [YouTube Sponsorship Tracker: Brand Deals, Promo Codes](https://apify.com/transparent_meteorite/youtube-sponsorship-tracker) | which YouTubers a brand sponsors, with promo codes and links | $2.00 |

## TikTok, Instagram and Threads

Public profiles, posts and comments, no login.

| Actor | What it does | Price per 1,000 results |
|---|---|---|
| [TikTok Profile Scraper: Followers, Videos, Bio Email](https://apify.com/transparent_meteorite/tiktok-public-profile-scraper) | public TikTok profiles and latest posts, bio links and emails | $2.50 |
| [TikTok Scraper: Hashtags, Search, Sounds, Places, Profiles](https://apify.com/transparent_meteorite/tiktok-hashtag-search-scraper) | TikTok hashtag, keyword, sound and place feeds | $2.10 |
| [TikTok Comments Scraper: Replies, Likes, Commenters](https://apify.com/transparent_meteorite/tiktok-comments-scraper) | comments and replies from public TikTok videos | $0.87 |
| [Instagram Profile Scraper: Followers, Bio Links, Emails](https://apify.com/transparent_meteorite/instagram-public-profile-scraper) | public Instagram profiles: followers, bio links, emails in bio | $1.82 |
| [Instagram Reels Scraper: Plays, Comments, Music](https://apify.com/transparent_meteorite/instagram-reels-scraper) | reels from public Instagram accounts with plays and comments | $1.50 |
| [Threads Scraper: Profiles, Posts, Views, Likes](https://apify.com/transparent_meteorite/threads-profile-scraper) | public Threads profiles and posts with views and likes | $1.50 |

---

Data comes from public pages, official open-data portals and public APIs. You are responsible for using it within each source's terms and applicable privacy law.
