'use client'

import Image from 'next/image'

export default function About() {
  return (
    <section id="about" className="px-4 md:px-8 lg:px-12 pb-16">
      <div className="mx-auto max-w-6xl grid gap-8 md:grid-cols-2 items-center">
        <div className="rounded-3xl h-72 md:h-96 bg-gradient-to-br from-amber-100 to-yellow-100 shadow-lg flex items-center justify-center relative overflow-hidden" data-aos="fade-right">
          <div className="relative w-full h-full">
            <Image
              src="https://images.unsplash.com/photo-1600891964599-f61ba0e24092?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
              alt="Restaurant Kitchen"
              fill
              className="object-cover rounded-3xl"
            />
          </div>
          {/* Animated background elements */}
          <div className="absolute inset-0 opacity-10 pointer-events-none">
            <div className="absolute top-4 left-4 text-2xl">🍕</div>
            <div className="absolute top-8 right-8 text-xl">🌮</div>
            <div className="absolute bottom-8 left-8 text-xl">🌶️</div>
          </div>
        </div>
        <div data-aos="fade-left">
          <h3 className="text-2xl md:text-3xl font-semibold mb-3">Our Story</h3>
          <p className="text-neutral-700 leading-relaxed">
            Simple Place started as a tiny home kitchen, obsessed with bold Mexican flavors and Vietnamese herbs. The result: joyful pizza with taco toppings, served in a sunny yellow space.
          </p>
          <div className="mt-4 flex items-center gap-2 text-amber-600" aria-label="5 out of 5 stars">
            {[...Array(5)].map((_, i) => (
              <span key={i} className="hover:scale-110 transition-transform">★</span>
            ))}
            <span className="text-sm text-neutral-500 ml-2">Loved by 2,000+ diners</span>
          </div>
        </div>
      </div>
    </section>
  )
}
