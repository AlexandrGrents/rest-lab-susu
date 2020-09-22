let table = document.getElementById('main');

let selectedType = document.getElementById('type')

function show(keys, elems)
{
	for (let i=table.children.length; i>=0; i--) if (table.children[i]) table.children[i].remove();
	let tr = document.createElement('tr');
	let td, btn;
	for (let key of keys)
	{
		td = document.createElement('td');
		td.innerHTML = '<b>' + key+ '</b>';
		tr.append(td);
	}
	table.append(tr);
	for (let elem of elems)
	{
		tr = document.createElement('tr');
		for (let key of keys)
		{
			td = document.createElement('td');
			td.innerText = elem[key];
			td.dataset.key = key;
			tr.append(td);
		}

		td = document.createElement('td');
		btn = document.createElement('button')
		btn.innerText = 'update';
		console.log(elem)
		btn.dataset.id = elem.id;
		btn.dataset.name = selectedType.value;
		btn.onclick = updateElem;
		td.append(btn)
		tr.append(td)

		td = document.createElement('td');
		btn = document.createElement('button')
		btn.innerText = 'delete';
		console.log(elem)
		btn.dataset.id = elem.id;
		btn.dataset.name = selectedType.value;
		btn.onclick = delElem;
		td.append(btn)
		tr.append(td)


		table.append(tr);
	}
	tr = document.createElement('tr');

	let input
	for (let key of keys)
	{
		td = document.createElement('td');
		console.log(key, key =='id')
		if (key == 'id')
		{
			td.innerText = 'auto'
			
		}
		else
		{
			input = document.createElement('input')

			input.name = key
			input.type = 'text'
			td.append(input);
		}
		tr.append(td)
	}

	td = document.createElement('td');
	btn = document.createElement('button')
	btn.innerText = 'create';
	btn.dataset.name = selectedType.value;
	btn.onclick = createElem;
	td.append(btn)
	tr.append(td)

	table.append(tr)

}

async function createElem(e)
{
	let elemType = e.target.dataset.name;
	let body = {};
	let tr = e.target.parentElement.parentElement;
	let value;
	for (let td of tr.children)
	{
		if (td.children.length ==0) continue;
		if (td.children[0].type == 'text')
		{
			value = parseInt(td.children[0].value);
			if (value)
				body[td.children[0].name] = value
			else body[td.children[0].name] = td.children[0].value;
		}
	}
	console.log(body)
	let response = await fetch('/api/' + elemType, {
		method: 'POST',
		headers:{
			'Content-type': 'application/json'
		},
		body: JSON.stringify(body)
	})
	if (response.ok) console.log('elem created')
		else console.log('err');
}

async function delElem(e)
{
	let elemType = e.target.getAttribute('data-name');
	let elemId = e.target.getAttribute('data-id');
	let response = await fetch('/api/' + elemType + '/' + elemId, {
		method: 'DELETE'
	})
	if (response.ok)
	{
		console.log('elem deleted');
	}
	else{
		console.log('err')
	}
}

async function updateElem(e)
{
	let tr = e.target.parentElement.parentElement;
	for (let td of tr.children)
	{
		if (td.dataset.key)
		{
			if (td.dataset.key == 'id')
			{
				continue
			}
			else
			{
				td.innerHTML = `<input type="text" name="${td.dataset.key}" value="${td.innerText}">`;
			}
		}
	}
	e.target.innerText = 'ok';
	e.target.onclick = patchElem

}

async function patchElem(e)
{
	let elemType = e.target.dataset.name;
	let body = {};
	let tr = e.target.parentElement.parentElement;
	let elemId = e.target.dataset.id;
	let value;
	for (let td of tr.children)
	{
		if (td.children.length ==0) continue;
		if (td.children[0].type == 'text')
		{
			value = parseInt(td.children[0].value);
			if (value)
				body[td.children[0].name] = value
			else body[td.children[0].name] = td.children[0].value;
		}
	}
	console.log(body)
	let response = await fetch('/api/' + elemType + '/' + elemId, {
		method: 'PATCH',
		headers:{
			'Content-type': 'application/json'
		},
		body: JSON.stringify(body)
	})
	if (response.ok) 
		{console.log('elem patched')
		changeView(tr);
}
		else console.log('err');
}

function changeView(tr)
{
	for (let td of tr.children)
	{
		if (td.children.length == 0) continue;
		else if (td.children[0].type == 'text')
		{
			td.innerHTML = td.children[0].value;
		}
		else if (td.children[0].innerText == 'ok')
		{
			td.children[0].innerText = 'update';
			td.children[0].onclick = updateElem;
		}
	}
}

selectedType.onchange = async () =>
{
	let value = selectedType.value;
	let response = await fetch('/api/' + value + '/all');
	let result = await response.json();
	console.log(result)
	if (result.length !== 0)
	{
		show(Object.keys(result[0]), result);
	}
}
selectedType.onchange();


async function f()
{
	let response = await fetch('/api/item', {
		method: 'POST',
		headers:{
			'Content-type': 'application/json'
		},
		body: JSON.stringify({
			name:'арбалет',
			owner:1,
			quality:95,
			itemType:1
		})
	})
	let result = await response.json();
	console.log(result);
	return result;
}
// f();