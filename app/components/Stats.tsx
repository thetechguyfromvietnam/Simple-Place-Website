'use client'

import { useEffect, useRef } from 'react'

export default function Stats() {
  const statsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number')
            statNumbers.forEach((stat) => {
              const target = parseInt(stat.getAttribute('data-count') || '0')
              const duration = 2000
              const increment = target / (duration / 16)
              let current = 0

              const updateStat = () => {
                current += increment
                if (current < target) {
                  stat.textContent = Math.floor(current).toString()
                  requestAnimationFrame(updateStat)
                } else {
                  stat.textContent = target.toString()
                }
              }

              updateStat()
            })
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.5 }
    )

    if (statsRef.current) {
      observer.observe(statsRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section className="px-4 md:px-8 lg:px-12 py-16 bg-gradient-to-r from-amber-50 to-yellow-50">
      <div className="mx-auto max-w-6xl">
        <div ref={statsRef} className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div className="stat-item" data-aos="fade-up" data-aos-delay="200">
            <div className="text-4xl md:text-5xl font-bold text-amber-600 stat-number" data-count="2000">0</div>
            <div className="text-sm text-neutral-600 mt-2">Happy Customers</div>
          </div>
          <div className="stat-item" data-aos="fade-up" data-aos-delay="400">
            <div className="text-4xl md:text-5xl font-bold text-amber-600 stat-number" data-count="50">0</div>
            <div className="text-sm text-neutral-600 mt-2">Unique Dishes</div>
          </div>
          <div className="stat-item" data-aos="fade-up" data-aos-delay="600">
            <div className="text-4xl md:text-5xl font-bold text-amber-600 stat-number" data-count="5">0</div>
            <div className="text-sm text-neutral-600 mt-2">Years of Service</div>
          </div>
          <div className="stat-item" data-aos="fade-up" data-aos-delay="800">
            <div className="text-4xl md:text-5xl font-bold text-amber-600 stat-number" data-count="98">0</div>
            <div className="text-sm text-neutral-600 mt-2">% Satisfaction</div>
          </div>
        </div>
      </div>
    </section>
  )
}
