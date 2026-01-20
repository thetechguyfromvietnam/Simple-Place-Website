'use client'

import Image from 'next/image'
import Link from 'next/link'

export default function Hero() {
  return (
    <section className="relative isolate min-h-[600px] flex items-center">
      <div className="absolute inset-0 -z-10">
        <Image
          src="/images/background.jpg"
          alt="Simple Place Restaurant"
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-b from-amber-500/20 via-black/40 to-black/70"></div>
      </div>
      
      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="floating-element absolute top-20 left-10 text-amber-300 text-6xl opacity-20">🍕</div>
        <div className="floating-element absolute top-40 right-20 text-amber-300 text-4xl opacity-20">🌮</div>
        <div className="floating-element absolute bottom-40 left-20 text-amber-300 text-5xl opacity-20">🌯</div>
      </div>
      
      <div className="text-white w-full">
        <div className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 py-24 md:py-36">
          <span className="inline-block text-xs uppercase tracking-widest text-amber-300 slide-in-left" data-aos="fade-right" data-aos-delay="200">
            Mexico × Vietnam
          </span>
          <h1 className="text-4xl md:text-6xl font-semibold leading-tight slide-in-left mt-4" data-aos="fade-right" data-aos-delay="400">
            Homemade pizza, taco soul.
          </h1>
          <p className="text-white/90 mt-4 md:text-lg max-w-2xl slide-in-left" data-aos="fade-right" data-aos-delay="600">
            A cheerful yellow kitchen famous for pizza topped with taco goodness — elote corn, lemongrass chicken, and fish‑sauce caramel vibes.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-3" data-aos="fade-up" data-aos-delay="800">
            <button 
              onClick={() => {
                const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
                dialog?.showModal()
              }}
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
            >
              Reserve Table
            </button>
            <Link href="#menu" className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-white/70 text-white hover:bg-white/10 text-center">
              See menu
            </Link>
            <a 
              href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true" 
              target="_blank" 
              rel="noopener" 
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-white text-amber-700 hover:bg-amber-50 text-center"
            >
              Order online →
            </a>
          </div>
          <div className="mt-5 text-sm text-amber-200 fade-in-up" data-aos="fade-up" data-aos-delay="1000">
            Open today: 10:00–22:00
          </div>
        </div>
      </div>
      {/* Wave divider */}
      <svg className="-mb-1 w-full text-neutral-50 absolute bottom-0" viewBox="0 0 1440 80" fill="currentColor" aria-hidden="true">
        <path d="M0,32L80,26.7C160,21,320,11,480,21.3C640,32,800,64,960,69.3C1120,75,1280,53,1360,42.7L1440,32L1440,80L1360,80C1280,80,1120,80,960,80C800,80,640,80,480,80C320,80,160,80,80,80L0,80Z"></path>
      </svg>
    </section>
  )
}
