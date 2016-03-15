# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from re import compile


class Alumno(models.Model):
    _name = 'sysnotas.alumno'
    _rec_name = "cui"

    cui = fields.Integer(string="CUI",
                         required=True,
                         index=True
                         )

    nombre = fields.Char(string="Nombre",
                         size=30,
                         required=True
                         )

    apellido = fields.Char(string="Apellidos",
                           size=30,
                           required=True
                           )

    observacion = fields.Text(string="Observación",
                              help="Observaciones al alumno "
                              )

    foto = fields.Binary(string="Foto")

    _sql_constraints = [
        ('alum_cui_uniq',
         'UNIQUE (cui)',
         'El CUI no puede repetirse!')]

    @api.one
    @api.constrains('nombre')
    def check_value_re(self):
        pattern = compile("^[a-zA-Z]+[\sa-zA-Z]*$")
        if not pattern.match(self.nombre):
            msg = 'El campo Nombre sólo puede tener letras!'
            raise ValidationError(msg)

    @api.one
    @api.constrains('cui')
    def alum_cui_check(self):
        pattern = compile("^[1-9]{1}[0-9]{7}$")
        if not pattern.match(str(self.cui)):
            msg = "El campo CUI debe tener 8 números !"
            raise ValidationError(msg)


class Curso(models.Model):
    _name = 'sysnotas.curso'
    _rec_name = "curso_nombre"

    curso_codigo = fields.Integer(string="Codigo Curso",
                                  required=True,
                                  index=True
                                  )

    curso_nombre = fields.Char(string="Nombre Curso",
                               size=30,
                               required=True
                               )

    creditos = fields.Integer(string="Créditos",
                              help="Cantidad de créditos"
                              )

    curs_comp = fields.Char(string="Relacion de Horas",
                            compute="_show"
                            )

    # relaciones
    curs_matr_cod = fields.Many2many('sysnotas.matricula',
                                     string='matr_cod'
                                     )

    curso_horario_rel = fields.One2many('sysnotas.curso_horario',
                                        'curso',
                                        string='Relacion de horas'
                                        )

    _sql_constraints = [
        ('curs_cod_unique',
         'UNIQUE (curso_codigo)',
         'El codigo del curso no puede repetirse!')]

    @api.one
    @api.depends('curso_horario_rel')
    def _show(self):
        self.curs_comp = " "
        str_aux = " "
        for c in self.curso_horario_rel:
            if str_aux == " " or str_aux != str(c.dia):
                self.curs_comp += " "+str(c.dia) + "->"
            self.curs_comp += "{0} - {1} {2} /".format(
                str(c.horaini),
                str(c.horafin),
                str(c.tipo_horario.denominacion))
            str_aux = str(c.dia)


class Matricula (models.Model):
    _name = 'sysnotas.matricula'
    _rec_name = "codigo"

    codigo = fields.Integer(string="Código",
                            help="Código de matrícula",
                            index=True
                            )

    nombre_alumno = fields.Text(string="Nombre",
                                store=False,
                                compute='make_nombre'
                                )

    # relaciones
    alumno = fields.Many2one('sysnotas.alumno',
                             string='Cui de Alumno'
                             )

    matr_curs_cod = fields.Many2many('sysnotas.curso',
                                     string='Cursos'
                                     )

    # sql constraints
    _sql_constraints = [
        ('matr_cod_unique',
         'UNIQUE (codigo)',
         'El codigo de matricula no puede repetirse!')]

    @api.one
    @api.depends('alumno')
    def make_nombre(self):
        print 'Entre'
        if self.alumno:
            self.nombre_alumno = "{0} {1}".format(self.alumno.nombre,
                                                  self.alumno.apellido)


class TipoHorario(models.Model):
    _name = 'sysnotas.tipohorario'
    _rec_name = 'denominacion'

    denominacion = fields.Char(string="Siglas",
                               required=True,
                               size=2,
                               index=True,
                               help="Ejemplo: TE, LB, TP "
                               )

    _sql_constraints = [
        ('tiph_deno_unique',
         'UNIQUE (denominacion)',
         'Ya existe tipo!')]


class CursoHorario(models.Model):
    _name = 'sysnotas.curso_horario'
    _rec_name = 'dia'

    tipo_horario = fields.Many2one('sysnotas.tipohorario',
                                   string='Tipo'
                                   )

    horaini = fields.Selection([(t, str(t)+":00") for t in range(0, 24)],
                               default=0)

    horafin = fields.Selection([(t, str(t)+":00") for t in range(0, 24)],
                               default=0)

    curso = fields.Many2one('sysnotas.curso',
                            string="Relación curso hora"
                            )

    dia = fields.Selection([
        ('Lunes', "Lunes"),
        ('Martes', "Martes"),
        ('Miercoles', "Miercoles"),
        ('Jueves', "Jueves"),
        ('Viernes', "Viernes")],
        default='Lunes')


class Wizard(models.TransientModel):
    _name = 'sysnotas.wizard'

    identi = fields.Integer(string="cod")
    matricula_id = fields.Many2one('sysnotas.matricula',
                                   string="Session",
                                   required=True
                                   )

    cantidad_cursos = fields.Integer(string="cant_cursos",
                                     compute="make_len",
                                     store=True
                                     )

    @api.one
    @api.depends('matricula_id')
    def make_len(self):
        if self.matricula_id:
            self.cantidad_cursos = len(self.matricula_id.matr_curs_cod)


class reported(models.TransientModel):
    _name = 'sysnotas.reported'

    rep_curso_nombre = fields.Char(string="Nombre Curso",
                                   size=30,
                                   required=True
                                   )
    rep_dia = fields.Char(string="Dia",
                          size=30,
                          required=True
                          )
    h0 = fields.Integer(string="h00")

    h1 = fields.Integer(string="h01")

    h2 = fields.Integer(string="h02")

    h3 = fields.Integer(string="h03")

    h4 = fields.Integer(string="h04")

    h5 = fields.Integer(string="h05")

    h6 = fields.Integer(string="h06")

    h7 = fields.Integer(string="h07")

    h8 = fields.Integer(string="h08")

    h9 = fields.Integer(string="h09")

    h10 = fields.Integer(string="h10")

    h11 = fields.Integer(string="h11")

    h12 = fields.Integer(string="h12")

    h13 = fields.Integer(string="h13")

    h14 = fields.Integer(string="h14")

    h15 = fields.Integer(string="h15")

    h16 = fields.Integer(string="h16")

    h17 = fields.Integer(string="h17")

    h18 = fields.Integer(string="h18")

    h19 = fields.Integer(string="h19")

    h20 = fields.Integer(string="h20")

    h21 = fields.Integer(string="h21")

    h22 = fields.Integer(string="h22")

    h23 = fields.Integer(string="h23")


class ParticularReport(models.AbstractModel):
    _name = 'report.sysnotas.report_curso_view'

    @api.multi
    def render_html(self, data=None):
        self.env['sysnotas.reported'].search([]).unlink()
        cursos = self.env['sysnotas.curso'].search([])
        dic_curso = {}
        tabla_curso = {}
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
        for curso in cursos:
            dic_curso_hora = {}
            tabla_dia = {}
            for curso_hora in curso.curso_horario_rel:
                if not dic_curso_hora.has_key(curso_hora.dia):
                    dic_curso_hora[curso_hora.dia] = []
                dic_curso_hora[curso_hora.dia].extend(
                    [(x) for x in range(
                        curso_hora.horaini, curso_hora.horafin)])
            for date in dias:
                tabla_dia[date] = {(x): 0 for x in range(0, 24)}
            tabla_curso[curso.curso_codigo] = tabla_dia
            dic_curso[curso.curso_codigo] = dic_curso_hora
        matri = self.env['sysnotas.matricula'].search([])
        for matricula in matri:
            for curso in matricula.matr_curs_cod:
                dic_dias = dic_curso[curso.curso_codigo]
                for dia in dias:
                    if dic_dias.has_key(dia):
                        for hora in dic_dias[dia]:
                            tabla_curso[curso.curso_codigo][dia][hora] += 1
        wizz = self.env['sysnotas.reported'].search([])
        for curso in cursos:
            for dia in dias:
                if tabla_curso[curso.curso_codigo].has_key(dia):
                    horas_wizard = {}
                    horas_wizard['rep_curso_nombre'] = curso.curso_nombre
                    horas_wizard['rep_dia'] = dia
                    for hora in range(0, 24):
                        horas_wizard['h'+str(hora)] = tabla_curso[curso.curso_codigo][dia][hora]
                    wizz.create(horas_wizard)
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sysnotas.report_curso_view')
        docargs = {
            'doc_ids': tuple(self.env['sysnotas.reported'].search([]).ids),
            'doc_model': report.model,
            'docs': self.env['sysnotas.reported'].search([]),
        }
        return report_obj.render('sysnotas.report_curso_view', docargs)
