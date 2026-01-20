'use client'

export default function Specials() {
  return (
    <section id="specials" className="px-4 md:px-8 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <div className="specials-banner rounded-2xl shadow-lg p-5 md:p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-3" data-aos="zoom-in">
          <div>
            <h2 className="text-2xl md:text-3xl font-semibold text-amber-800">Pizza × Tacos Weekly Specials</h2>
            <p className="text-amber-700">Ask for the Saigon Elote or the Bánh Mì Supreme this week.</p>
          </div>
          <div className="flex gap-2">
            <a
              href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true"
              target="_blank"
              rel="noopener"
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
            >
              Order now
            </a>
            <button
              onClick={() => {
                const dialog = document.getElementById('booking-dialog') as HTMLDialogElement
                dialog?.showModal()
              }}
              className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50"
            >
              Reserve
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
