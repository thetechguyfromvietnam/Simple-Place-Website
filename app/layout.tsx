import type { Metadata } from 'next'
import { Sora } from 'next/font/google'
import './globals.css'
import 'aos/dist/aos.css'

const sora = Sora({ 
  subsets: ['latin'],
  weight: ['400', '600', '700'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Simple Place — Pizza × Tacos Fusion',
  description: 'Simple Place: Homemade pizza with tacos — Mexico × Vietnam fusion in Saigon. Reserve a table or order online.',
  themeColor: '#f59e0b',
  openGraph: {
    title: 'Simple Place — Pizza × Tacos Fusion',
    description: 'Homemade pizza with tacos — reserve a table or order online.',
    images: ['https://images.unsplash.com/photo-1601924572345-0050bd436b0b?q=80&w=1200&auto=format&fit=crop'],
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Restaurant",
              "name": "Simple Place",
              "servesCuisine": ["Pizza", "Mexican", "Vietnamese", "Fusion"],
              "address": {
                "@type": "PostalAddress",
                "streetAddress": "215B4 Nguyễn Văn Hưởng, phường An Khánh",
                "addressLocality": "Thủ Đức, Thành phố Hồ Chí Minh",
                "addressRegion": "HCMC",
                "addressCountry": "VN"
              },
              "telephone": "+84 904421089",
              "menu": "https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true",
              "acceptsReservations": true
            })
          }}
        />
      </head>
      <body className={`${sora.className} antialiased text-neutral-900 bg-neutral-50`}>
        {children}
      </body>
    </html>
  )
}
