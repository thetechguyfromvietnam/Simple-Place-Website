'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-30 bg-white/80 backdrop-blur border-b">
      <nav className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 h-16 flex items-center justify-between">
        <Link href="/" className="font-semibold text-lg tracking-tight flex items-center gap-2 hover:scale-105 transition-transform duration-300">
          <span className="inline-block h-3 w-3 rounded-full bg-amber-500 float-animation"></span>
          <span>Simple Place</span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-6 text-sm">
          <Link href="#menu" className="nav-link hover:opacity-80">Menu</Link>
          <Link href="#about" className="nav-link hover:opacity-80">About</Link>
          <Link href="#visit" className="nav-link hover:opacity-80">Visit</Link>
          <Link href="#contact" className="nav-link hover:opacity-80">Contact</Link>
        </div>

        <div className="hidden md:flex items-center gap-2">
          <a 
            href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true" 
            target="_blank" 
            rel="noopener" 
            className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
          >
            Order Online
          </a>
          <button 
            onClick={() => {
              const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
              dialog?.showModal()
            }}
            className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50"
          >
            Reserve Table
          </button>
        </div>

        {/* Mobile hamburger */}
        <button 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden inline-flex items-center justify-center h-10 w-10 rounded-xl border text-neutral-700 hover:bg-amber-50 transition-colors"
          aria-expanded={mobileMenuOpen}
          aria-label="Toggle menu"
        >
          ☰
        </button>
      </nav>

      {/* Mobile menu panel */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-white/95 backdrop-blur">
          <div className="mx-auto max-w-6xl px-4 py-3 flex flex-col gap-3 text-sm">
            <Link href="#menu" className="py-2 hover:text-amber-600 transition-colors">Menu</Link>
            <Link href="#about" className="py-2 hover:text-amber-600 transition-colors">About</Link>
            <Link href="#visit" className="py-2 hover:text-amber-600 transition-colors">Visit</Link>
            <Link href="#contact" className="py-2 hover:text-amber-600 transition-colors">Contact</Link>
            <div className="flex gap-2 pt-2">
              <a 
                href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true" 
                target="_blank" 
                rel="noopener" 
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600 flex-1 text-center"
              >
                Order Online
              </a>
              <button 
                onClick={() => {
                  const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
                  dialog?.showModal()
                  setMobileMenuOpen(false)
                }}
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50 flex-1"
              >
                Reserve Table
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
