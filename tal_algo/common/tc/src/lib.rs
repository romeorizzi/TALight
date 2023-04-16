use std::env; 
use std::path::Path;
use std::fs;
use std::io::{stdout, Write};
use std::time;

pub type Pippo<'a, T> = &'a [(u32, T)];
pub struct TC<'a, T> {
    data: Pippo<'a, T>,
    time_limit: time::Duration,
    exam: bool,    
}

impl<T> TC<'_, T> {
    pub fn new(data: Pippo<T>, time_limit: time::Duration) -> TC<T> {
        let exam = env::vars().filter(|(key,val)|
                        ["TAL_META_EXP_TOK ","TAL_EXT_EXAM_DB"].contains(&&key[..])).count() == 2;

        TC {data, time_limit, exam}
    }

    pub fn run<F1,F2,R>(&self, gen_tc: F1, check_tc: F2)
    where
        F1: Fn(&T) -> R, 
        F2: Fn(R) -> Result<Option<String>,&'static str>,
    {
        let path_result = Path::new(&env::var_os("TAL_META_OUTPUT_FILES")
                                    .expect("expected envairoment var TAL_META_OUTPUT_FILES"))
                                    .join("result.txt");
        let mut f_result = fs::File::create(path_result).expect("qualcosa");
        let tot_tc: u32 = self.data.iter().map(|(n, _)|n).sum();
        println!("{tot_tc}");
        stdout().flush();
        let (mut tc_ok, mut tcn) = (0, 1);
        for subtask in 0..self.data.len() {
            for tc in 0..self.data[subtask].0 {
                let tc_data = gen_tc(&self.data[subtask].1);
                stdout().flush();
                let t_start = time::Instant::now();

                let ret = check_tc(tc_data);
                let late = t_start.elapsed() > self.time_limit;

                match ret.as_ref() {
                    Ok(res) => match res {
                        _ if late => { writeln!(f_result, "Case #{tcn:03}: TLE"); },
                        Some(_) => { writeln!(f_result, "Case #{tcn:03}: WA"); },
                        None => {
                            writeln!(f_result, "Case #{tcn:03}: AC");
                            tc_ok += 1;
                        },
                    }
                    Err(e) => { writeln!(f_result, "Case #{tcn:03}: RE"); },
                }

                let feedback = match ret {
                    Ok(res) => res,
                    Err(e) => Some(String::from(e)),
                };
                if let Some(msg) = feedback {
                    writeln!(f_result, "\n{msg}\n");
                }
                tcn += 1;
            }
        }
        writeln!(f_result);
        writeln!(f_result, "Score: {tc_ok}/{tot_tc}");
    }
}


