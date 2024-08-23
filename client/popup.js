chrome.storage.local.get(['sortingMethod'], (result) => {
	if (result.sortingMethod) {
		sortItems(result.sortingMethod[0], result.sortingMethod[1])
	}
})

console.log(document.querySelector('main').children)

function sortItems(option, type = 'asc') {
	const elementsToSort = Array.from(document.querySelector('main').children)
	document.querySelector('main').innerHTML = ''

	if (type === 'asc') {
		if (option === 'price') {
			elementsToSort
				.sort(
					(a, b) =>
						+a.children[1].children[1].children[1].children[0].children[0]
							.innerHTML -
						+b.children[1].children[1].children[1].children[0].children[0]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		}
	} else if (type === 'desc') {
		if (option === 'price') {
			elementsToSort
				.sort(
					(a, b) =>
						+b.children[1].children[1].children[1].children[0].children[0]
							.innerHTML -
						+a.children[1].children[1].children[1].children[0].children[0]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		} else if (option === 'rating') {
			elementsToSort
				.sort(
					(a, b) =>
						+b.children[1].children[1].children[0].children[0].children[1]
							.innerHTML -
						+a.children[1].children[1].children[0].children[0].children[1]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		}
	}

	chrome.storage.local.set({ sortingMethod: [option, type] })
}

document
	.querySelector('.dropdown-item.dropdown-item__price-desc')
	.addEventListener('click', () => {
		sortItems('price', 'desc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__price-asc')
	.addEventListener('click', () => {
		sortItems('price', 'asc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__rating-desc')
	.addEventListener('click', () => {
		sortItems('rating', 'desc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__delivery-time-asc')
	.addEventListener('click', () => {
		sortItems('deliveryTime', 'asc')
	})
