use std::i32;
use std::cmp::min;

fn compute(mut input_list: Vec<i32>, offset: usize, phases: i32) -> String {
    let mut result: Vec<i32> = Vec::new();

    for phase in 0..phases {
        let mut output_list = input_list.clone();

        let mut first_time = true;
        let mut previous_output= 0;
        let start = offset;

        for i in start..input_list.len() {
            let mut output = previous_output;

            if i < input_list.len() / 2 {
                let mut index = i;
                let repeat = index + 1;
                let jump = repeat * 4;

                while index < input_list.len() {
                    for k in index..min(index + repeat, input_list.len()) {
                        output += input_list[k];
                    }
                    index += jump;
                }

                index = i + repeat * 2;
                while index < input_list.len() {
                    for k in index..min(index + repeat, input_list.len()) {
                        output -= input_list[k];
                    }
                    index += jump;
                }

                output_list[i] = i32::abs(output) % 10;
            } else {
                if first_time {
                    for index in i..input_list.len() {
                        output += input_list[index];
                    }
                    first_time = false;
                } else {
                    output -= input_list[i - 1];
                }

                previous_output = output;
                output_list[i] = output % 10;
            }
        }

        if phase == phases - 1 {
            result = output_list.clone();
        }
        input_list = output_list;
    }

    result[offset..offset + 8].iter().map(|i| i.to_string()).collect::<String>()
}

fn main() {
    let input_str = "59787832768373756387231168493208357132958685401595722881580547807942982606755215622050260150447434057354351694831693219006743316964757503791265077635087624100920933728566402553345683177887856750286696687049868280429551096246424753455988979991314240464573024671106349865911282028233691096263590173174821612903373057506657412723502892841355947605851392899875273008845072145252173808893257256280602945947694349746967468068181317115464342687490991674021875199960420015509224944411706393854801616653278719131946181597488270591684407220339023716074951397669948364079227701367746309535060821396127254992669346065361442252620041911746738651422249005412940728";

    let input: Vec<i32> = input_str.chars().map(|c| c.to_digit(10).unwrap() as i32).collect();

    let mut input_list = input.clone();

    println!("{}", compute(input_list.clone(), 0, 100));

    for _ in 0..9999 {
        input_list.append(&mut input.clone());
    }

    let offset = input_str[..7].parse::<usize>().unwrap();
    println!("{}", compute(input_list.clone(), offset, 100));
}
