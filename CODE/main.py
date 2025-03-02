import os, sys, term, time, termcolor, argparse, random; from term import *
parser = argparse.ArgumentParser(prog='tbi');parser.add_argument('file', help='the TBI file to run');parser.add_argument('-s', '--slow', help='run each instruction every 0.2 seconds', action='store_true');parser.add_argument('-l', '--labeldata', help='show line count, rg, isl, and rline in bottom left corner', action='store_true');parser.add_argument('-d', '--data', help=f'writes data on-screen as: {termcolor.colored('fs', 'yellow')}, {termcolor.colored('reg', 'green')}, {termcolor.colored('args', 'blue')}, {termcolor.colored('linecount', 'red')}', action='store_true')
args = parser.parse_args();reg = [0, 0, 0, 0, 0, 0, 0, 0];disk1 = {'fileMode': 1, 'fileSystem': {'stdout': '', 'nco': 0, 'eco': 0, 'gm': 0, 'ncc':-2, 'ecc': -2, 'icn': [0, 0]}};flags = {'run': True};rg = {};rline = 0;isl = False
while True:
    file = args.file
    if os.path.exists(file):break
    else:print('no such file');exit()
I=round;G=range
def A(yse,xse,title='Box',text=[''],sx=25,sy=8):
	saveCursor()
	J=title;F=yse;E=sx;D='on_blue';C='white';A=xse
	for B in G(A,E+A):
		pos(F,B+1)
		if B==A:write(termcolor.colored('┌',C,D))
		elif B==A+E-1:write(termcolor.colored('┐',C,D))
		else:write(termcolor.colored('─',C,D))
	for K in G(F+1,F+sy):
		for B in G(A,E+A):
			pos(K,B+1)
			if B==A:write(termcolor.colored('│',C,D))
			elif B==A+E-1:write(termcolor.colored('│',C,D))
			else:write(termcolor.colored(' ',C,D))
	for B in G(A,E+A):
		pos(F+sy,B+1)
		if B==A:write(termcolor.colored('└',C,D))
		elif B==A+E-1:write(termcolor.colored('┘',C,D))
		else:write(termcolor.colored('─',C,D))
	L=I(E/2)-I(len(J)/2)+2;pos(F,L+A);write(termcolor.colored(J,C,D));H=0
	for M in text:H=H+1;pos(F+H,2+A);write(termcolor.colored(M,C,D))
	restoreCursor()
term.homePos(); term.clear(); term.setTitle('tbi'); term.setTab('tbi')
with open(file, 'r') as fi:fcont = fi.read()
cont = -1; eva = [False, False, False, False, False, False, False, False]
def decodeFunc(inp, lc):return inp.split('\n')[lc].split('`')
while flags['run']:
    if not cont + 1 == len(fcont.split('\n')):
        cont = cont + 1; i = fcont.split('\n')[cont]; e = i.split('`')
        try:
            if args.slow:time.sleep(0.2)
            if args.labeldata:term.saveCursor();tsize = term.getSize()[0];term.pos(tsize,0);term.clearLine();term.write(termcolor.colored(cont, 'red')+', '+termcolor.colored(rg, 'green')+', '+termcolor.colored(isl, 'blue')+', '+termcolor.colored(rline, 'yellow'));term.restoreCursor()
            if args.data:term.saveCursor();tsize = term.getSize()[0];term.pos(tsize,0);term.clearLine();term.write(termcolor.colored(reg, 'green') + ', ' + termcolor.colored(e, 'blue') + ', ' + termcolor.colored(cont, 'red') + ', ' + termcolor.colored(eva, 'yellow'));term.pos(tsize-1,0);term.clearLine();term.write(termcolor.colored(disk1['fileSystem'], 'magenta'));term.restoreCursor()
            if e[0] == 'rg':reg[int(e[1])] = e[2].replace(':NL:', '\n')
            elif e[0] == 'ri':reg[int(e[1])] = input().replace(':NL:', '\n')
            elif e[0] == 'ng':
                eva = [False, False, False, False, False, False, False, False];trx = e[2]
                for i in range(len(reg)):trx = trx.replace(f'[r{i}]', f'int(reg[{i}])')
                try:reg[int(e[1])] = int(eval(trx))
                except Exception as ex:
                    for i in range(len(reg)):
                        try: eva[i] = True;te = eval(reg[i])
                        except: eva[i] = True;continue
                        if eva[i] == True: trx = trx.replace(f'int(reg[{i}])', f'{eval(reg[i])}')
                reg[int(e[1])] = eval(trx)
            elif e[0] == 'ra':reg[int(e[1])] = str(reg[int(e[1])]) + e[2].replace(':NL:', '\n')
            elif e[0] == 'mv':disk1['fileSystem'][e[2]] = reg[int(e[1])]
            elif e[0] == 'gt':reg[int(e[1])] = disk1['fileSystem'][e[2]]
            elif e[0] == 'mr':reg[int(e[1])] = random.randint(int(reg[int(e[2])]), int(reg[int(e[3])]))
            elif e[0] == 'su':
                if int(disk1['fileSystem']['gm']) == 1: term.pos(reg[6], reg[7])
                term.write(str(disk1['fileSystem']['stdout']))
            elif e[0] == 'jmp':
                if e[1].startswith(':'):rline = cont;isl = True;cont = rg[e[1]]['s']
                else:cont = int(e[1])
            elif e[0] == 'lp': econt = int(e[2]);ncont = int(e[1]);disk1['fileSystem']['eco'] = econt;disk1['fileSystem']['nco'] = ncont
            elif e[0] == 'brk': disk1['fileSystem']['eco'] = -2;disk1['fileSystem']['nco'] = -2
            elif e[0] == 'if': econt = int(e[2]);ncont = int(e[1]);disk1['fileSystem']['ecc'] = econt;disk1['fileSystem']['ncc'] = ncont;disk1['fileSystem']['icn'][0] = int(e[3]);disk1['fileSystem']['icn'][1] = int(e[4])
            elif e[0] == 'gm': disk1['fileSystem']['gm'] = 1
            elif e[0] == 'rc':reg[int(e[1])] = reg[int(e[2])]
            elif e[0] == 'ex': A(2,2,'Exit program', ['Press enter to exit']); pos(term.getSize()[0], term.getSize()[1]); input(); clear(), exit()
            elif e[0] == 'dl':
                try:time.sleep(float(reg[int(e[1])]))
                except:print(f'[exception-handler]: ignoring Exception (NotImplemented: floating-point values aren\'t supported)');continue
            elif e[0].startswith(':') and not e[0] == ':END':
                rg[e[0]] = {'s': cont, 'e': 1};tcount = 0
                while not decodeFunc(fcont, tcount+cont)[0] == ':END': tcount = tcount + 1
                rg[e[0]] = {'s': cont, 'e': tcount+cont};cont = tcount+cont+1
            for i in list(rg.values()):
                if i['e'] == cont and isl:isl = False;cont = rline
            if cont == disk1['fileSystem']['eco']: cont = disk1['fileSystem']['nco']
            if cont == disk1['fileSystem']['ncc'] and not reg[int(disk1['fileSystem']['icn'][0])] == reg[int(disk1['fileSystem']['icn'][1])]:cont = disk1['fileSystem']['ecc']
        except Exception as ex:
            print(f'[exception-handler]: ignoring Exception ({ex})')
            continue
