function greet() {
  return "hello world!";
}

const quarterOf = (month) => {
  if (Math.ceil(month / 3) == 1){
        return 1;
    } else if (Math.ceil(month / 3) == 2){
        return 2;
    } else if (Math.ceil(month / 3) == 3){
        return 3;
    } else if (Math.ceil(month / 3) == 4){
        return 4;
    }
}

function capitalizeWord(word) {
  return word.replace(word[0], String(word.toUpperCase()[0]));
}

function century(year) {
  return Math.ceil(year / 100);
}

function numberToString(num) {
  return String(num);
}

const stringToNumber = function(str){
  return str * 1;
}

function toBinary(n){
  return (n >>> 0).toString(2) * 1;
}

function evenOrOdd(number) {
  if (number % 2 == 0){
    return "Even";
  } else {
    return 'Odd';
  }
}

function areaLargestSquare(r) {
  return 2 * Math.pow(r, 2);
}

function digits(n) {
  return String(n).length * 1;
}

function opposite(number) {
  return number * -1;
}

function removeChar(str){
  return str.slice(1, str.length - 1);
}


function noSpace(x){
  return x.replaceAll(' ', '');
}

function simpleMultiplication(number) {
  if (number % 2 == 0){
    return number * 8;
  } else {
    return number * 9;
  }
}

function repeatStr (n, s) {
  return s.repeat(n);
}

function finalGrade (exam, projects) {
  if (exam > 90 || projects > 10){
    return 100;
  } else if (exam > 75 && projects >= 5){
    return 90;
  } else if (exam > 50 && projects >= 2){
    return 75;
  } else {
    return 0;
  }
}

function updateLight(current) {
  if (current == "green"){
    return 'yellow';
  } else if (current == "yellow"){
    return 'red';
  } else if (current == "red"){
    return "green";
  }
}

function otherAngle(a, b) {
  return 180 - a - b;
}

function rentalCarCost(d) {
  if (d >= 7){
    return 40 * d - 50;
  } else if (d >= 3){
    return 40 * d - 20;
  } else{
    return 40 * d;
  }
}

function typeOfSum(a, b) {
  return typeof(a+b);
}

const zeroFuel = (distanceToPump, mpg, fuelLeft) => {
  return (distanceToPump <= mpg * fuelLeft);
}

function perimeterSequence(a,n) {
  return a * n * 4;
}

