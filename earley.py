class EarleyParser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []

    def parse(self, text):
        self.states = [set() for _ in range(len(text) + 1)]
        self.states[0].add(State(*grammar.start))

        for k, token in enumerate(text + '\u0000'):
            extension = list(self.states[k])
            self.states[k].clear()

            while extension:
                state = extension.pop()
                if state in self.states[k]:
                    continue

                self.states[k].add(state)

                if state.finished:
                    self._completer(state, extension)
                elif state.symbol_is_nonterminal:
                    self._predictor(state, k, extension)
                else:
                    self._scanner(state, k, token)

        self._print(text)

    def _predictor(self, state, origin, extension):
        for rule in self.grammar[state.symbol]:
            extension.append(State(*rule, origin=origin))

    def _scanner(self, state, origin, token):
        if state.symbol == token:
            self.states[origin + 1].add(state.shift)

    def _completer(self, state, extension):
        for reduce in self.states[state.origin]:
            if state.nonterminal == reduce.symbol:
                extension.append(reduce.shift)

    def _print(self, text):
        for k, state in enumerate(self.states):
            accepts = any(s.nonterminal == '^' and s.finished for s in state)

            print('(%d)' % k, end=' ')
            print('"%s.%s"' % (text[:k], text[k:]), end=' ')
            print(accepts and 'ACCEPTS' or '')

            for i in state:
                print('\t', i)


class State:

    def __init__(self, nonterminal, expression, dot=0, origin=0):
        self.nonterminal = nonterminal
        self.expression = expression
        self.dot = dot
        self.origin = origin

    @property
    def finished(self):
        return self.dot >= len(self.expression)

    @property
    def symbol(self):
        return None if self.finished else self.expression[self.dot]

    @property
    def symbol_is_nonterminal(self):
        return self.symbol and self.symbol.isalpha() and self.symbol.isupper()

    @property
    def shift(self):
        return State(self.nonterminal, self.expression, self.dot + 1, self.origin)

    @property
    def tuple(self):
        return self.nonterminal, self.expression, self.dot, self.origin

    def __hash__(self):
        return hash(self.tuple)

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __str__(self):
        n, e, d, o = self.tuple
        return '[%d] %s -> %s.%s' % (o, n, e[:d], e[d:])


class Grammar:

    def __init__(self, *rules):
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('::='))
        
    @property
    def start(self):
        return next(self['^'])

    def __getitem__(self, nonterminal):
        yield from [rule for rule in self.rules if rule[0] == nonterminal]



grammar = Grammar(
    '^ ::= E',
    'E ::= E + T',
    'E ::= E - T',
    'E ::= T',
    'T ::= T * F',
    'T ::= T / F',
    'T ::= F',
    'F ::= ( E )',
    'F ::= - F',
    'F ::= x',
    'F ::= y',
    'F ::= z',
)

gramatica=Grammar(

'^ ::= S',
'S ::= SentenciaCual | SentenciaQuien | SentenciaQue | SentenciaDonde | SentenciaCuanto | SentenciaComo | SentenciaPorque',

'SentenciaCual ::= SentenciaCualTarget | SentenciaCualPlatoTipico | SentenciaCualProcedimiento',
'SentenciaCualTarget ::= ProCual VSer SNRecetaIngrediente SPrepEntidadPlato',
'SentenciaCualPlatoTipico ::= ProCual VSer SNComida SPrepEntidadLocalidad | ProCual VSer SNComida SubordinadoLocalidad',
'SentenciaCualProcedimiento ::= ProCual VSer SNProcedimiento PrepDePara SVPrepararPlato | ProCual VSer SNProcedimiento SubordinadoPlato',

'SentenciaQuien ::= ProQuien VInventar SEntidadPlato',

'SentenciaQue ::= SentenciaQueProcedimiento | SentenciaQueIngrediente | SentenciaQueDefinicion',
'SentenciaQueProcedimiento ::= ProQue SubProcedimiento VerboAuxPreparar SEntidadPlato | ProQue SubProcedimiento VerboAuxUtilizar PrepPara SVPrepararPlato',
'SentenciaQueIngrediente ::= ProQue TargetIngrediente VerboAuxUtilizar PrepPara SVPrepararPlato | ProQue TargetIngrediente VTener SEntidadPlato | ProQue TargetIngrediente VerboAuxTener', 'SEntidadPlato',
'SentenciaQueDefinicion ::= ProQue VSer SEntidadPlato | ProQue VSer SEntidadIngrediente',

'SentenciaDonde ::= SentenciaDondeConseguir | SentenciaDondeEsHecho | SentenciaDondeConseguir AdjuntoLocalidad | SentenciaDondeEsHecho AdjuntoLocalidad',
'SentenciaDondeConseguir ::= ProDonde VerboAuxComprar SEntidadPlato | ProDonde VerboAuxComprar SEntidadPlato SPrepEntidadLocalidad',
'SentenciaDondeEsHecho ::= ProDonde VerboAuxProducir SEntidadPlato | ProDonde VerboAuxEncontrar SEntidadPlato',

'SentenciaCuanto ::= SentenciaCuantoUnidades | SentenciaCuantoResiste | SentenciaCuantoTiempo',
'SentenciaCuantoUnidades ::= ProCuanto UnidadesIngredientes SVNecesitarPrepararPlato',
'SentenciaCuantoResiste ::= ProCuanto VResistir SEntidadPlato',
'SentenciaCuantoTiempo ::= ProCuanto SubTiempo VResistir SEntidadPlato',

'SentenciaComo ::= ProComo VerboRefPreparar SEntidadPlato',

'SentenciaPorque ::= PrepPor ProQue Motivo',
'Motivo ::=  SujetoEntidad SVerbal | SVerbal SujetoEntidad',
'MotivoMenor ::=  SNominal SVerbal',
'SujetoEntidad ::=  SujetoPlato | SujetoIngrediente',
'SujetoPlato ::=  SEntidadPlato | SNominal Prep SEntidadPlato | SEntidadPlato Prep SNominal',
'SujetoIngrediente ::=  SEntidadIngrediente |  SNominal Prep SEntidadIngrediente | SEntidadIngrediente Prep SNominal',
'SNominal ::=  Sub | Det Sub | Sub Adj | Det Sub Adj | ProRef',
'SVerbal ::=  Verbo SNominal | Verbo SNominal ProRel MotivoMenor',

'SPrepEntidadPlato ::= PrepDe SEntidadPlato | PrepEn SEntidadPlato',
'SPrepEntidadLocalidad ::= PrepDe SEntidadLocalidad | PrepEn SEntidadLocalidad',

'SNProcedimiento ::= SubProcedimiento | Det SubProcedimiento',
'SNRecetaIngrediente ::= SNReceta | SNIngrediente | SNIngrediente PrepDe SNReceta | SNReceta PrepDe SNIngrediente',
'SNReceta ::= SubReceta | Det SubReceta | SubReceta AdjPrincipal | Det SubReceta AdjPrincipal',
'SNIngrediente ::= SubIngrediente | Det SubIngrediente | SubIngrediente AdjPrincipal | Det SubIngrediente AdjPrincipal',
'SNComida ::= SubComida | Det SubComida | SubComida AdjPrincipal | Det SubComida AdjPrincipal',

'TargetIngrediente ::= SubIngrediente | SubTipo PrepDe EntidadIngrediente',
'UnidadesIngredientes ::= SubIngrediente | SubMedida PrepDe EntidadIngrediente',

'SubordinadoLocalidad ::= ProRel VerboIdentificar SEntidadLocalidad',
'SubordinadoPlato ::= ProRel VerboAuxPreparar SEntidadPlato | PrepEn ProRel VerboAuxPreparar SEntidadPlato',
'SEntidadLocalidad ::= EntidadLocalidad | Det EntidadLocalidad',
'SEntidadIngrediente ::= EntidadIngrediente | Det EntidadIngrediente',
'SVPrepararPlato ::= VPreparar SEntidadPlato',
'SVNecesitarPrepararPlato ::= VNecesitarRef PrepPara VPreparar EntidadPlato | VNecesitar SEntidadPlato',

'SEntidadPlato ::= EntidadPlato | Det EntidadPlato | DetIndefinido SubPlato PrepDe EntidadPlato',
'VerboAuxPreparar ::= ProRef VDeber VPreparar | VDeber VPreparar',
'VerboRefPreparar ::= VPreparar | ProRef VPreparar | VDeber VPreparar',
'VerboAuxUtilizar ::= ProRef VDeber VUtilizar | ProRef VUtilizar | VDeber VUtilizar',
'VerboAuxComprar ::= ProRef VDeber VComprar | ProRef VComprar | VDeber VComprar | VComprar',
'VerboAuxTener ::= ProRef VDeber VTener | VDeber VTener',
'VerboAuxProducir ::= ProRef VProducir | ProRef VDeber VProducir | VDeber VProducir | VProducir',
'VerboAuxEncontrar ::= ProRef VEncontrar | VEncontrar | VDeber VEncontrar',
'VNecesitarRef ::= ProRef VNecesitar',
'AdjuntoLocalidad ::= AdjuntoLugar EntidadLocalidad',
'AdjuntoLugar ::= PrepEn | AdjCerca PrepDe | PrepAl SubLado PrepDe',

'Verbo ::= <*,*,va,> | <*,*,vmi,> | <*,*,vs,>',
'Sub ::= <*,*,nc,>',
'Det ::= DetDefinido | DetIndefinido',
'Conj ::= <*,*,cc,>',
'Prep ::= <*,*,sp,>',
'Pro ::= <*,*,pt,>',
'Entidad ::= <,,,*>',
'Adj ::= <*,*,aq,>',

'ProCual ::= <*,cuál,,>',
'ProQuien ::= <*,quién,,>',
'ProQue ::= <*,que,,>',
'ProDonde ::= <*,donde,,>',
'ProCuanto ::= <*,cuánto,,>',
'ProComo ::= <*,cómo,,>',
'DetDefinido ::= <*,*,da,>',
'DetIndefinido ::= <*,*,di,>',
'EntidadPlato ::= <*,,,PLATO>',
'EntidadLocalidad ::= <*,,,LOCALIDAD>',
'EntidadIngrediente ::= <*,,,INGREDIENTE>',
'PrepDe ::= <*,de,sp,>',
'PrepEn ::= <*,en,sp,>',
'PrepPara ::= <*,para,sp,>',
'PrepDePara ::= <*,para,sp,>',
'PrepAl ::= <*,al,np,>',
'PrepPor ::= <*,por,np,>',
'SubIngrediente ::= <*,ingrediente,nc,>',
'SubReceta ::= <*,receta,nc,>',
'SubPlato ::= <*,postre,nc,> | <*,plato,nc,>',
'SubComida ::= <*,postre,nc,> | <*,plato,nc,> | <*,comida,nc,>',
'SubTipo ::= <*,clase,nc,> | <*,tipo,nc,>',
'SubLado ::= <*,lado,nc,> | <*,costado,nc,>',
'SubMedida ::= <*,unidad,nc,> | <*,kilo,nc,> | <*,onza,nc,> | <*,dozena,nc,>',
'SubTiempo ::= <*,tiempo,nc,>',
'AdjPrincipal ::= <*,principal,aq,> | <*,típico,aq,>',
'AdjCerca ::= <*,cerca,aq,> | <*,próximo,aq,>',
'ProRel  ::= <*,que,pr,>',
'SubProcedimiento ::= <*,procedimiento,nc,> | <*,forma,nc,> | <*,temperatura,nc,> | <*,cocción,nc,> | <*,manera,nc,>',
'VSer ::= <*,ser,vmi,>',
'VInventar ::= <*,inventar,vmi,>',
'VPreparar ::= <*,preparar,vmi,> | <*,cocinar,vmi,> | <*,hacer,vmi,> | <*,hornear,vmi,>',
'ProRef ::= <*,*,p,> | <*,*,pp,>',
'VerboIdentificar  ::= <*,identificar,vmi,> | <*,caracterizar,vmi,>',
'VDeber ::= <*,deber,vmi,> | <*,poder,vmi,> | <*,tener,vmi,> | <*,recomendar,vmi,> | <*,sugerir,vmi,>',
'VUtilizar ::=  <*,usar,vmi,> | <*,utilizar,vmi,> | <*,aplicar,,> ',
'VTener ::=  <*,tener,vmi,> | <*,llevar,vmi,>',
'VComprar ::=  <*,comprar,vmi,>',
'VProducir ::=  <*,producir,vmi,> | <*,hacer,vmi,> | <*,cocinar,vmi,> | <*,prepar,vmi,>',
'VEncontrar ::=  <*,encontrar,vmi,>',
'VNecesitar ::=  <*,necesitar,vmi,>',
'VResistir ::=  <*,resistir,vmi,>'
)
EarleyParser(gramatica).parse('cómo se prepara un plato de ají de gallina')



