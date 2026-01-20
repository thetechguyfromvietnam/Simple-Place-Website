# Simple Place Website

Modern Next.js website for Simple Place restaurant with booking system and menu management.

## Features

- 🍕 **Full Menu Display** - Complete menu with categories and filtering
- 📅 **Table Reservation** - Booking system with Google Sheets integration
- 🎨 **Modern UI/UX** - Beautiful animations and responsive design
- ⚡ **Fast Performance** - Optimized with Next.js 14 and TypeScript
- 📱 **Mobile First** - Fully responsive design
- 🎯 **Best Sellers** - Featured items highlighting

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: AOS (Animate On Scroll) + Framer Motion
- **Deployment**: Vercel
- **Data**: JSON files for menu management

## Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Set up environment variables**:
Create a `.env.local` file:
```
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY=your-private-key
GOOGLE_SHEET_ID=your-google-sheet-id
```

3. **Run development server**:
```bash
npm run dev
```

4. **Build for production**:
```bash
npm run build
npm start
```

## Google Sheets Setup for Bookings

1. Create a Google Sheet with columns: Timestamp, Name, Email, Phone, Date/Time, Guests, Message
2. Create a Google Service Account
3. Share the Google Sheet with the service account email
4. Add credentials to `.env.local`

## Deployment to Vercel

1. Push code to GitHub
2. Import project to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy!

## Project Structure

```
├── app/
│   ├── api/
│   │   └── booking/        # Booking API route
│   ├── components/         # React components
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── data/
│   └── menu.json          # Menu data
├── public/
│   └── images/            # Static images
└── vercel.json            # Vercel configuration
```

## License

© 2025 Simple Place. All rights reserved.
