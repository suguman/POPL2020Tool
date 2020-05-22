never {
accept_init:
  if
  :: (((!(x_a0)) && (x_a1) && (!(y_set_x_a0)) && (!(y_set_x_a1))) || ((x_a0) && (!(x_a1)) && (!(y_set_x_a0)) && (!(y_set_x_a1)))) -> goto accept_all
  :: (((!(x_a0)) && (x_a1) && (y_set_x_a0) && (!(y_set_x_a1))) || ((x_a0) && (!(x_a1)) && (!(y_set_x_a0)) && (y_set_x_a1))) -> goto T0_S2
  :: ((x_a0) && (!(x_a1)) && (y_set_x_a0)) -> goto accept_S3
  :: ((!(x_a0)) && (x_a1) && (y_set_x_a1)) -> goto accept_S4
  fi;
T0_S2:
  if
  :: (true) -> goto T0_S2
  fi;
accept_S3:
  if
  :: (((!(x_a0)) && (x_a1) && (!(y_set_x_a0))) || ((x_a0) && (!(x_a1)) && (!(y_set_x_a0)))) -> goto accept_all
  :: ((!(x_a0)) && (x_a1) && (y_set_x_a0)) -> goto T0_S2
  :: ((x_a0) && (!(x_a1)) && (y_set_x_a0)) -> goto T0_S5
  fi;
accept_S4:
  if
  :: (((!(x_a0)) && (x_a1)) || ((x_a0) && (!(x_a1)))) -> goto accept_all
  fi;
T0_S5:
  if
  :: (((!(x_a0)) && (x_a1) && (!(y_set_x_a0))) || ((x_a0) && (!(x_a1)) && (!(y_set_x_a0)))) -> goto accept_all
  :: ((!(x_a0)) && (x_a1) && (y_set_x_a0)) -> goto T0_S2
  :: ((x_a0) && (!(x_a1)) && (y_set_x_a0)) -> goto T0_S5
  fi;
accept_all:
  skip
}
