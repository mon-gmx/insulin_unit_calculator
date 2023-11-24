function getUnits(carbs, sugar) {

  let units = 0;
  let bedtime_units = 18;
  
  // if no data is present no data should return
  if ((carbs == null && sugar == null) || (carbs == 0 && sugar == 0)) {
    return null;
  }

  /*
  
  all corner cases are defined here, midnight measurements,
  bedtime long-lasting insulin and out of range sugar and carbs
  including warnings 
  
  */
  
  if (carbs == "MIDNIGHT" || carbs == "midnight") {
    return 0;
  }

  if (carbs == "BEDTIME" || carbs == "bedtime") {
    return bedtime_units;
  }

  if (carbs > 200) {
    return "TOO MANY CARBS! CHECK VALUES";
  }
  
  if (sugar < 70 || sugar == "LOW" || sugar == "low") {
    return "SUGAR IS LOW, CARBS NEEDED TO COMPENSATE!";
  }

  if(sugar > 630) {
    return "SUGAR IS DANGEROUSLY HIGH! GET TO ER";
  }

  /*
  
  carbs tabulation as passed in the sheet, this is not
  elegant code but is easy to read and modify

  */
  
  if (carbs >= 8 && carbs < 16) {
    units += 1;
  } else if (carbs >= 16 && carbs < 24) {
    units += 2;
  } else if (carbs >= 24 && carbs < 32) {
    units += 3;
  } else if (carbs >= 32 && carbs < 40) {
    units += 4;
  } else if (carbs >= 40 && carbs < 48) {
    units += 5;
  } else if (carbs >= 48 && carbs < 56) {
    units += 6;
  } else if (carbs >= 56 && carbs < 64) {
    units += 7;
  } else if (carbs >= 64 && carbs < 72) {
    units += 8;
  } else if (carbs >= 72 && carbs < 80) {
    units += 9;
  } else if (carbs >= 80 && carbs < 88) {
    units += 10;
  } else if (carbs >= 88 && carbs < 96) {
    units += 11;
  } else if (carbs >= 96 && carbs < 104) {
    units += 12;
  } else if (carbs >= 104 && carbs < 112) {
    units += 13;
  } else if (carbs >= 112 && carbs < 120) {
    units += 14;
  } else if (carbs >= 120 && carbs < 128) {
    units += 15;
  } else if (carbs >= 128 && carbs < 136) {
    units += 16;
  } else if (carbs >= 136 && carbs < 144) {
    units += 17;
  } else if (carbs >= 144 && carbs < 152) {
    units += 18;
  } else if (carbs >= 152 && carbs < 160) {
    units += 19;
  } else if(carbs == 160) {
    units += 20;
  }

  /*
  
  sugar tabulation as passed in the sheet, this is not
  elegant code but is easy to read and modify
  
  */

  if (sugar >= 70 && sugar <= 100) {
    units -= 1;
  } else if(sugar >= 101 && sugar <= 150) {
    units += 0;
  } else if(sugar >= 151 && sugar <= 190) {
    units += 1;
  } else if(sugar >= 191 && sugar <= 230) {
    units += 2;
  } else if(sugar >= 231 && sugar <= 270) {
    units += 3;
  } else if(sugar >= 271 && sugar <= 310) {
    units += 4;
  } else if(sugar >= 311 && sugar <= 350) {
    units += 5;
  } else if(sugar >= 351 && sugar <= 390) {
    units += 6;
  } else if(sugar >= 391 && sugar <= 430) {
    units += 7;
  } else if(sugar >= 431 && sugar <= 470) {
    units += 8;
  } else if(sugar >= 471 && sugar <= 510) {
    units += 9;
  } else if(sugar >= 511 && sugar <= 550) {
    units += 10;
  } else if(sugar >= 551 && sugar <= 590) {
    units += 11;
  } else if(sugar >= 591 && sugar <= 630) {
    units = 12;
  } 

  // units should return as calculated with adjustment
  return units;
}
