function save_match(label){

  var match_label = document.getElementById(label).value
  var team_1 = parseInt(document.getElementById(label + 'team_1').value)
  var team_2 = parseInt(document.getElementById(label + 'team_2').value)
  var penals_1 = parseInt(document.getElementById(label + 'penals_1').value)
  var penals_2 = parseInt(document.getElementById(label + 'penals_2').value)
  var token = document.getElementsByName("csrfmiddlewaretoken")[0].value
  var check = check_inputs(team_1, team_2, penals_1, penals_2)

  if (check == true)
  {
    var headers = {'X-CSRFToken': token}
    var body = {
              'match_label': match_label.slice(0, -1),
              'team_1' : team_1,
              'team_2': team_2,
              'penals_1': penals_1,
              'penals_2': penals_2
          }
    var authOptions = {
                      method: 'POST',
                      url: '/guardar_partido/',
                      data: body,
                      headers: headers,
                      json: true
                      }

    axios(authOptions)
      .then(function (response) {
        alert('Se ha guardado el partido')
      })
  }
}

function check_inputs(team_1, team_2, penals_1, penals_2){

  if (isNaN(team_1) || isNaN(team_2) || team_1 < 0 || team_2 < 0){
    alert('Verifica el valor de los goles')
    return false
  }
  else if(isNaN(penals_1) || isNaN(penals_2) || penals_1 < 0 || penals_2 < 0){
    alert('Verifica el valor de los penales')
    return false
  }
  else if(team_1 != team_2 && (penals_1 >0 || penals_2 > 0)){
    alert('Los penales no son necesarios, verifica por favor')
    return false
  }
  else if(team_1 == team_2 && ((penals_1 < 0 || penals_2 < 0) || (penals_1 == penals_2))){
    alert('Asegúrate de que los penales definan un ganador')
    return false
  }

  else{
    return true
  }
}
