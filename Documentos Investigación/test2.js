/* Aquí va la programación del test */

function labelradio (nombre, valor, texto){
	var r = $(document.createElement('input')).attr('type', 'radio')
	.attr('name', nombre).attr('value', valor).attr('required', 'required'); // TODO: Reactivar "required"
	var l = $(document.createElement('label')).append(r).append(texto);
	return l;
}

function br (){
	return $(document.createElement('br'));
}

function valorRadio (listaDeNodos){
	for (var i = 0; i < listaDeNodos.length; i++){
		var item = listaDeNodos[i];
		if (item.checked){
			return item.value;
		}
	}
	return false;
}


function creapregunta (numero){
	actividad = actividades[numero];

	var nombre = 'actividad' + numero;
	actividad['formnombre'] = nombre;

	var l = $(document.createElement('legend')).text(actividad['actividad']);
	var set = $(document.createElement('fieldset'));
	set.append (l);
	set.append (labelradio (nombre, '5', 'Me gusta mucho')).append(br());
	set.append (labelradio (nombre, '4', 'Me gusta')).append(br());
	set.append (labelradio (nombre, '3', 'Me es indiferente')).append(br());
	set.append (labelradio (nombre, '2', 'No me gusta')).append(br());
	set.append (labelradio (nombre, '1', 'Me desagrada mucho')).append(br());

	return set;
}



function procesaform (){
		// validar todas las preguntas
		// desactivar formulario
		// sumar puntuaciones
		// pasar al siguiente formulario

		f = $(this);

		// validar
		for (var i = 0; i < preguntasPorHoja && actual + i < actividades.length; i++) {
			var a = actividades[actual + i];
			var nombre = a['formnombre'];
			var valor = valorRadio (this[nombre]);
			//alert (a['actividad'] + valor);
			if (! valor){
				alert ('Seleccione una opción en pregunta "' + a['actividad'] + '"');
				// ¿Enfocarse o hacer scroll hacia la pregunta?
				return false;
			}
		}

		// desactivar formulario
		f.off('submit');
		f.submit(function(event){ return false; });

		// sumar puntuaciones
		for (var i = 0; i < preguntasPorHoja && actual + i < actividades.length; i++) {
			var a = actividades[actual + i];
			var nombre = a['formnombre'];
			var valor = valorRadio (this[nombre]);
			puntajes[a['tema']] += parseInt(valor);
		}

		// pasar al siguiente formulario
		actual += preguntasPorHoja;
		f.fadeOut (400, function(){
			pregunta();
		});

		return false;
}

function creaform (){
	var f = $(document.createElement('form'));

	//
	// Meter grupo de preguntas con funcion creapregunta
	//

	for (var i = 0; i < preguntasPorHoja && actual + i < actividades.length; i++) {
		var pregunta = creapregunta (actual + i);
		f.append (pregunta);
		f.append (br());
	};


	var b = $(document.createElement('button')).text('Siguiente').attr('type', 'submit');
	f.append(b);
	f.submit (procesaform);
	return f;
}


function encuentraPorciento (tabla, puntos){
	for (var i = 0; i < tabla.length; i++) {
		var par = tabla[i];
		if (par['pts'] >= puntos){
			return par['%'];
		}
	}
	// Si no se encuentra, retornar con 100 %
	return '100';
}

function buscaPorcentaje (tema, sexo, puntos){
	var t = tabla[tema];
	var s = t[sexo];
	return encuentraPorciento(s, puntos);
}


function resultados (){
	var d = $(document.createElement('div'));
	for (var tema in puntajes){
		var p = buscaPorcentaje (tema, sexo, puntajes[tema]);
		var n = $(document.createElement('p')).append (tema + ' : ' + p + '%').append(br());
		d.append(n);
	}
	return d;
}



function resultados_porcentaje (){
	var r = new Array();
	for (var tema in puntajes){
		var t = new Object();
		t['n'] = tema;
		t['%'] = buscaPorcentaje (tema, sexo, puntajes[tema]);
		r.push(t);
	}
	return r;
}

function ordenatemas (a, b){
	return a['%'] - b['%'];
}

function resultados2 (){
	var r = resultados_porcentaje();
	r.sort(ordenatemas);
	r.reverse();
	return r;
}


function muestra_resultados (){
	var r = resultados2();
	var u = $(document.createElement('ul'));
	u.addClass('pestanas');
	for (var i = 0; i < r.length; i++){
		var t = r[i];
		var tema = temas[t['n']];
		var n = $(document.createElement('a')).append (tema['nombre'] + ': ' + t['%'] + '%').append(br());
		idtema = '#' + tema['idcontenido'];
		n.addClass(t['n']);
		n.attr('href', idtema);
		var l = $(document.createElement('li'));
		l.append(n);
		u.append(l);
		if (i == 0){
			l.addClass('selected');
		}
	}
	var d = $(document.createElement('div'));

	muestra_temas();
	var areas = $('#areas');
	d.append (u);
	d.append (areas);

	return d;
}
function muestra_temas(){
	$('#areas').removeClass('oculto');
}

var actual = 0;
function pregunta (){
	if (actual >= actividades.length){
		// calcular el resultado aqui <--
		$('#interaccion').append(muestra_resultados());
		$('.pestanas').idTabs();
		return false;
	}
	var f = creaform();
	$('#interaccion').append(f);
	f.hide();
	f.fadeIn();
	return true;
}





function iniciatest (){
	var f = $('#formsexo');
	f.submit(function(event){

		sexo = valorRadio (this.sexo);
		if (sexo){

			$(this).off('submit');
			$(this).submit(function(event){ return false; });	// Así desactivamos formulario
			$(this).fadeOut(400, pregunta);
		} else {
			alert ('Seleccione una opción');
		}
		return false;
	});
	f.fadeIn();
}
