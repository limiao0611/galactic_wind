import yt


def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)

  c1 = [0.85,0.5,0.5]
  #c1=[0.545,0.599,0.602]
  #c1 =[0.891576, 0.130623, 0.186343]
  sp=ds.sphere(c1, (20, 'pc'))

  slc = yt.SlicePlot(ds, 'x', ['density','temperature','pressure'],center=c1).save()
  slc = yt.SlicePlot(ds, 'y', ['density','temperature','pressure'],center=c1).save()
  slc = yt.SlicePlot(ds, 'z', ['density','temperature','pressure'],center=c1).save()


num =[550,637]
for i in num:
   see(i)


