'use client'

import { useState } from 'react'

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // TODO: Connect to backend or Formspree/Resend
    setTimeout(() => {
      alert('Thanks! We\'ll reply by email.')
      setFormData({ name: '', email: '', message: '' })
      setIsSubmitting(false)
    }, 1000)
  }

  return (
    <section id="contact" className="px-4 md:px-8 lg:px-12 pb-28">
      <div className="mx-auto max-w-6xl grid gap-8 md:grid-cols-2 items-stretch">
        {/* Contact us */}
        <div className="rounded-2xl border bg-white p-5 flex flex-col justify-between hover:shadow-lg transition-shadow" data-aos="fade-up" data-aos-delay="200">
          <div>
            <h4 className="text-lg font-semibold">Contact us</h4>
            <p className="text-sm text-neutral-600">Questions, parties, or large orders? We&apos;ve got you.</p>
            <div className="mt-4 space-y-3 text-sm">
              <div className="flex items-center gap-2 hover:text-amber-600 transition-colors">
                <span>📞</span>
                <a className="hover:underline" href="tel:+84904421089">(+84) 904421089</a>
              </div>
              <div className="flex items-center gap-2 hover:text-amber-600 transition-colors">
                <span className="text-xl">💙</span>
                <a className="hover:underline" href="tel:+84904421089">(+84) 904421089</a>
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">Zalo</span>
              </div>
              <div className="flex items-center gap-2 hover:text-amber-600 transition-colors">
                <span>✉️</span>
                <a className="hover:underline" href="mailto:Tranmy077@gmail.com">Tranmy077@gmail.com</a>
              </div>
              <div className="flex items-center gap-2 hover:text-amber-600 transition-colors">
                <span className="text-xl">👥</span>
                <a className="hover:underline" href="https://www.facebook.com/simpleplacesaigon" target="_blank" rel="noopener noreferrer">Facebook</a>
              </div>
              <div className="flex items-center gap-2 hover:text-amber-600 transition-colors">
                <span className="text-xl">📸</span>
                <a className="hover:underline" href="https://www.instagram.com/simpleplacefusion/" target="_blank" rel="noopener noreferrer">Instagram</a>
              </div>
            </div>
          </div>
          <div className="mt-6 flex gap-2">
            <button
              onClick={() => {
                const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
                dialog?.showModal()
              }}
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
            >
              Reserve Table
            </button>
            <a
              href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true"
              target="_blank"
              rel="noopener"
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50"
            >
              Order online
            </a>
          </div>
        </div>

        {/* Private events */}
        <div className="rounded-2xl border bg-white p-5 flex flex-col justify-between hover:shadow-lg transition-shadow" data-aos="fade-up" data-aos-delay="400">
          <div>
            <h4 className="text-lg font-semibold">Private events</h4>
            <p className="text-sm text-neutral-600">Tell us about your event and we&apos;ll get back within one business day.</p>
          </div>
          <form onSubmit={handleSubmit} className="mt-4 space-y-3">
            <input
              className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
              placeholder="Your name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <input
              className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
              placeholder="Email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
            <textarea
              className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
              rows={5}
              placeholder="What are you planning? (date, group size, budget)"
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            />
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-enhanced w-full rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600 disabled:opacity-50"
            >
              {isSubmitting ? 'Submitting...' : 'Submit inquiry'}
            </button>
            <p className="text-xs text-neutral-500">Demo form — connect to your backend or Formspree/Resend.</p>
          </form>
        </div>
      </div>
    </section>
  )
}
