'use client'

import { useState } from 'react'

export default function BookingDialog() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date: '',
    time: '',
    guests: '2',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus('idle')

    try {
      const response = await fetch('/api/booking', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        setSubmitStatus('success')
        setFormData({
          name: '',
          email: '',
          phone: '',
          date: '',
          time: '',
          guests: '2',
          message: ''
        })
        setTimeout(() => {
          const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
          dialog?.close()
          setSubmitStatus('idle')
        }, 2000)
      } else {
        setSubmitStatus('error')
      }
    } catch (error) {
      console.error('Booking error:', error)
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <dialog id="booking-dialog" className="rounded-2xl p-0 max-w-md w-full backdrop:bg-black/55">
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold">Reserve a Table</h2>
          <button
            onClick={() => {
              const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
              dialog?.close()
            }}
            className="text-neutral-500 hover:text-neutral-700 text-2xl"
          >
            ×
          </button>
        </div>

        {submitStatus === 'success' ? (
          <div className="text-center py-8">
            <div className="text-5xl mb-4">✅</div>
            <p className="text-lg font-semibold text-green-600">Booking submitted successfully!</p>
            <p className="text-sm text-neutral-600 mt-2">We'll contact you soon to confirm.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                placeholder="Your name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Email *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                placeholder="your@email.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Phone *</label>
              <input
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                placeholder="+84 000 000 000"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Date *</label>
                <input
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Time *</label>
                <input
                  type="time"
                  required
                  value={formData.time}
                  onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                  min="10:00"
                  max="22:00"
                  className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Number of Guests *</label>
              <select
                required
                value={formData.guests}
                onChange={(e) => setFormData({ ...formData, guests: e.target.value })}
                className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                  <option key={num} value={num}>{num} {num === 1 ? 'guest' : 'guests'}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Special Requests</label>
              <textarea
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                rows={3}
                className="w-full rounded-xl border px-4 py-2 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all"
                placeholder="Any special requests or dietary requirements?"
              />
            </div>

            {submitStatus === 'error' && (
              <div className="text-red-600 text-sm">Failed to submit booking. Please try again.</div>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-enhanced w-full rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600 disabled:opacity-50"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Reservation'}
            </button>
          </form>
        )}
      </div>
    </dialog>
  )
}
