'use client'

import Link from 'next/link'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t bg-gradient-to-r from-amber-50 to-yellow-50">
      <div className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 py-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="text-sm text-neutral-600">© {currentYear} Simple Place. All rights reserved.</div>
          <div className="flex flex-col md:flex-row items-center gap-4">
            <div className="flex gap-4 text-sm text-neutral-600">
              <Link href="#about" className="hover:text-amber-600 transition-colors">About</Link>
              <Link href="#menu" className="hover:text-amber-600 transition-colors">Menu</Link>
              <Link href="#contact" className="hover:text-amber-600 transition-colors">Contact</Link>
            </div>
            <div className="flex items-center gap-4 text-neutral-600">
              <a 
                href="https://www.facebook.com/simpleplacesaigon" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-blue-600 transition-all transform hover:scale-110 text-2xl"
                aria-label="Facebook"
                title="Facebook"
              >
                👥
              </a>
              <a 
                href="https://www.instagram.com/simpleplacefusion/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-pink-600 transition-all transform hover:scale-110 text-2xl"
                aria-label="Instagram"
                title="Instagram"
              >
                📸
              </a>
              <a 
                href="tel:+84904421089" 
                className="hover:text-blue-500 transition-all transform hover:scale-110 text-2xl"
                aria-label="Zalo"
                title="Zalo Hotline"
              >
                💙
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
