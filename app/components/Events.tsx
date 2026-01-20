'use client'

import Image from 'next/image'

export default function Events() {
  return (
    <section id="events" className="px-4 md:px-8 lg:px-12 py-20 bg-gradient-to-br from-amber-50 via-yellow-50 to-amber-100">
      <div className="mx-auto max-w-6xl">
        <div className="text-center mb-12" data-aos="fade-up">
          <h2 className="text-4xl md:text-5xl font-bold text-amber-900 mb-4">Events & Promotions</h2>
          <p className="text-lg text-amber-700 max-w-2xl mx-auto">
            Don&apos;t miss out on our weekly specials and exciting promotions
          </p>
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          {/* Event Card */}
          <div
            className="group rounded-3xl bg-white shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-2"
            data-aos="fade-up"
            data-aos-delay="200"
          >
            <div className="relative h-64 overflow-hidden bg-gradient-to-br from-amber-100 to-yellow-100">
              <Image
                src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800&auto=format&fit=crop"
                alt="Taco Tuesday Event"
                fill
                className="object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute top-4 left-4">
                <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-amber-500 text-white shadow-lg">
                  🎉 Weekly Event
                </span>
              </div>
            </div>
            <div className="p-6 md:p-8">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-2xl md:text-3xl font-bold text-amber-900">Taco Tuesday</h3>
                <span className="text-3xl">🌮</span>
              </div>
              <p className="text-base text-neutral-700 mb-6 leading-relaxed">
                Join us every Tuesday for our special Taco Tuesday! Enjoy delicious tacos for only 45,000 VND each.
              </p>
              <div className="space-y-3 pt-4 border-t border-amber-200">
                <div className="flex items-center gap-3 text-neutral-700">
                  <span className="text-amber-600 text-xl">📅</span>
                  <span className="font-medium">Every Tuesday</span>
                </div>
                <div className="flex items-center gap-3 text-neutral-700">
                  <span className="text-amber-600 text-xl">🕐</span>
                  <span className="font-medium">10:00 AM – 10:00 PM</span>
                </div>
                <div className="flex items-center gap-3 text-amber-700 font-semibold mt-4">
                  <span className="text-2xl">💰</span>
                  <span className="text-lg">Only 45,000 VND per taco</span>
                </div>
              </div>
            </div>
          </div>

          {/* Promotion Card */}
          <div
            className="group rounded-3xl bg-white shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-2"
            data-aos="fade-up"
            data-aos-delay="400"
          >
            <div className="relative h-64 overflow-hidden bg-gradient-to-br from-red-100 to-orange-100">
              <Image
                src="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=800&auto=format&fit=crop"
                alt="Wednesday Pizza Promotion"
                fill
                className="object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute top-4 left-4">
                <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-red-500 text-white shadow-lg">
                  🔥 Special Offer
                </span>
              </div>
            </div>
            <div className="p-6 md:p-8">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-2xl md:text-3xl font-bold text-red-900">Pizza Wednesday</h3>
                <span className="text-3xl">🍕</span>
              </div>
              <p className="text-base text-neutral-700 mb-6 leading-relaxed">
                Every Wednesday, get 20% off on all pizzas! Perfect for sharing with friends and family.
              </p>
              <div className="space-y-3 pt-4 border-t border-red-200">
                <div className="flex items-center gap-3 text-neutral-700">
                  <span className="text-red-600 text-xl">📅</span>
                  <span className="font-medium">Every Wednesday</span>
                </div>
                <div className="flex items-center gap-3 text-neutral-700">
                  <span className="text-red-600 text-xl">🕐</span>
                  <span className="font-medium">10:00 AM – 10:00 PM</span>
                </div>
                <div className="flex items-center gap-3 text-red-700 font-semibold mt-4">
                  <span className="text-2xl">💸</span>
                  <span className="text-lg">20% off all pizzas</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
