---
name: nextjs-site-scaffold
description: Scaffold a new Next.js project with a full stack and set of conventions. Use this skill whenever starting a new website, web app, or frontend project. Triggers on "new project", "scaffold", "start a site", "set up Next.js", "create a new app", "init project", "create a new site", "spin up a project", "bootstrap", or any request to build a new website or application from scratch. Also triggers when user says "new client site", "start building", or names a brand + "website".
---

# Next.js Site Scaffold

A complete project scaffold for new Next.js applications. Every project starts from this foundation: TypeScript, Tailwind CSS, App Router, shadcn/ui, Framer Motion, GSAP, and a clean folder structure with brand-aware color tokens.

## Quick Start (Full Sequence)

Run these commands in order. The entire scaffold takes about 2 minutes.

### Step 1: Create the App

```bash
npx create-next-app@latest PROJECT_NAME \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
```

When prompted:
- Would you like to use Turbopack? **Yes**

### Step 2: Install Dependencies

```bash
cd PROJECT_NAME

# Animation & interaction
npm install framer-motion gsap @gsap/react

# Utility classes
npm install clsx tailwind-merge

# Icons (required by Aceternity UI components)
npm install @tabler/icons-react

# Class variance authority (used by shadcn)
npm install class-variance-authority
```

### Step 3: Initialize shadcn/ui

```bash
npx shadcn@latest init
```

When prompted:
- Style: **Default**
- Base color: **Neutral** (override per brand later)
- CSS variables: **Yes**

Install common base components:

```bash
npx shadcn@latest add button card dialog input label separator sheet
```

### Step 4: Create Folder Structure

```bash
# Core directories
mkdir -p src/components/ui        # shadcn components (auto-created by shadcn init)
mkdir -p src/components/sections  # Page sections (heroes, features, footers, CTAs)
mkdir -p src/components/effects   # Animation wrappers, scroll effects, transitions
mkdir -p src/components/games     # Game components (interactive/canvas projects)
mkdir -p src/lib                  # Utilities, hooks, helpers
mkdir -p src/styles               # Global styles, font config
mkdir -p src/assets               # Static images, SVGs
mkdir -p public/images            # Public static assets
mkdir -p public/fonts             # Self-hosted fonts (if needed)
```

### Step 5: Create Utility Files

**`src/lib/utils.ts`** (shadcn creates this, but verify it contains):

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**`src/lib/fonts.ts`** (default font pairing):

```typescript
import { Inter, Playfair_Display } from "next/font/google";

export const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
});
```

### Step 6: Set Up Root Layout

**`src/app/layout.tsx`**:

```tsx
import type { Metadata } from "next";
import { inter, playfair } from "@/lib/fonts";
import "./globals.css";

export const metadata: Metadata = {
  title: "PROJECT_NAME",
  description: "PROJECT_DESCRIPTION",
  openGraph: {
    title: "PROJECT_NAME",
    description: "PROJECT_DESCRIPTION",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
```

### Step 7: Configure Tailwind with Brand Tokens

In your `tailwind.config.ts` (or the CSS-based config in Tailwind v4), extend with brand colors. Choose the brand or use neutral defaults:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        serif: ["var(--font-playfair)", "Georgia", "serif"],
      },
      colors: {
        // Replace with your own brand tokens (see CSS vars below)
        brand: {
          primary: "var(--brand-primary)",
          secondary: "var(--brand-secondary)",
          accent: "var(--brand-accent)",
          muted: "var(--brand-muted)",
          background: "var(--brand-background)",
          foreground: "var(--brand-foreground)",
        },
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-in-out",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.5s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDown: {
          "0%": { transform: "translateY(-20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

Set the CSS variables in `src/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Default neutral brand tokens — override per project */
    --brand-primary: #0A2540;
    --brand-secondary: #3A8FB7;
    --brand-accent: #E8725C;
    --brand-muted: #F5E6D3;
    --brand-background: #FFFFFF;
    --brand-foreground: #0A2540;
  }

  .dark {
    --brand-background: #0A0A0A;
    --brand-foreground: #FAFAFA;
  }
}
```

### Step 8: Vercel Deployment Config

**`vercel.json`**:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

Deploy command:

```bash
npx vercel --prod
```

Or link and deploy via Git:

```bash
npx vercel link
git push  # Auto-deploys on push if linked
```

### Step 9: Environment Variables

**`.env.example`**:

```bash
# ===========================================
# Environment Variables — Copy to .env.local
# ===========================================

# App
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME="PROJECT_NAME"

# Analytics (optional)
NEXT_PUBLIC_GA_ID=
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=

# CMS (choose one)
# NEXT_PUBLIC_SANITY_PROJECT_ID=
# NEXT_PUBLIC_SANITY_DATASET=production
# NEXT_PUBLIC_NOTION_API_KEY=

# API Keys (server-side only — no NEXT_PUBLIC_ prefix)
# AIRTABLE_PAT=
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=

# Deployment
# VERCEL_PROJECT_ID=
# VERCEL_ORG_ID=
```

Copy it:

```bash
cp .env.example .env.local
```

### Step 10: ESLint Configuration

**`.eslintrc.json`**:

```json
{
  "extends": [
    "next/core-web-vitals",
    "next/typescript"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["warn", {
      "argsIgnorePattern": "^_",
      "varsIgnorePattern": "^_"
    }],
    "prefer-const": "warn",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  }
}
```

### Step 11: CLAUDE.md for the Project

Create a `CLAUDE.md` at the project root. Include: project overview, tech stack (Next.js App Router, TypeScript, Tailwind, shadcn/ui + Aceternity + Magic UI, Framer Motion, GSAP, @tabler/icons-react, Vercel), the folder structure from Step 4, dev commands (`npm run dev/build/lint`), and these conventions:

- Use `cn()` from `@/lib/utils` for conditional class merging
- Animation components go in `components/effects/`
- Page sections are self-contained in `components/sections/`
- Server Components by default; add `"use client"` only when needed
- Fonts loaded via `next/font` in `@/lib/fonts.ts`
- Brand colors use CSS variables (see globals.css)
- Push to main branch for automatic Vercel deployment

### Step 12: VS Code Extensions

**`.vscode/extensions.json`** — recommended extensions:

```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss", "esbenp.prettier-vscode", "dbaeumer.vscode-eslint",
    "formulahendry.auto-rename-tag", "christian-kohler.path-intellisense",
    "dsznajder.es7-react-js-snippets", "yoavbls.pretty-ts-errors", "usernamehw.errorlens"
  ]
}
```

**`.vscode/settings.json`** — format on save, ESLint auto-fix, Tailwind class detection for `cn()` and `cva()`:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": { "source.fixAll.eslint": "explicit" },
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

---

## Common Post-Scaffold Tasks

### Add UI Components (Aceternity + Magic UI)

```bash
# Aceternity UI — dramatic, scroll-driven effects
npx shadcn@latest add hero-parallax aurora-background spotlight lamp
npx shadcn@latest add floating-navbar bento-grid 3d-card

# Magic UI — polished, refined animations
npx shadcn@latest add aurora-text typing-animation number-ticker
npx shadcn@latest add shimmer-button marquee blur-fade particles
```

### Starter Effect Components

**GSAP ScrollTrigger** (`src/components/effects/scroll-section.tsx`):

```typescript
"use client";
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

export function ScrollSection({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  useGSAP(() => {
    gsap.from(".animate-in", {
      y: 60, opacity: 0, duration: 0.8, stagger: 0.15, ease: "power2.out",
      scrollTrigger: { trigger: ref.current, start: "top 80%", toggleActions: "play none none reverse" },
    });
  }, { scope: ref });
  return <div ref={ref}>{children}</div>;
}
```

**Framer Motion page wrapper** (`src/components/effects/page-transition.tsx`):

```typescript
"use client";
import { motion } from "framer-motion";

export function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.3, ease: "easeInOut" }}>
      {children}
    </motion.div>
  );
}
```

---

## Checklist

Use this to verify the scaffold is complete:

- [ ] `create-next-app` ran with all flags (TS, Tailwind, ESLint, App Router, src dir)
- [ ] Dependencies installed (framer-motion, gsap, @gsap/react, clsx, tailwind-merge, @tabler/icons-react, class-variance-authority)
- [ ] `npx shadcn@latest init` completed
- [ ] Base shadcn components added (button, card, dialog, input, label, separator, sheet)
- [ ] Folder structure created (components/ui, sections, effects, games; lib; styles; assets)
- [ ] `src/lib/utils.ts` has `cn()` function
- [ ] `src/lib/fonts.ts` has font configuration
- [ ] `src/app/layout.tsx` uses font variables and metadata
- [ ] `tailwind.config.ts` extended with brand colors and animations
- [ ] `globals.css` has CSS variable definitions
- [ ] `vercel.json` created
- [ ] `.env.example` created and copied to `.env.local`
- [ ] `.eslintrc.json` configured
- [ ] `CLAUDE.md` created at project root
- [ ] `.vscode/extensions.json` and `.vscode/settings.json` created
- [ ] Git initialized and initial commit made
- [ ] Brand-specific overrides applied (if building for a specific brand identity)

---

## References

- Cross-reference **component-catalog** skill for component install commands and page recipes
- Cross-reference **gsap-animation-patterns** skill for scroll-driven animation patterns
- Cross-reference **framer-motion-patterns** skill for interaction animation patterns
