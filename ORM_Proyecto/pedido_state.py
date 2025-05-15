
class EstadoPedido:
    def avanzar(self, pedido):
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def cancelar(self, pedido):
        raise NotImplementedError("Este método debe ser implementado por las subclases.")


class EstadoNuevo(EstadoPedido):
    def avanzar(self, pedido):
        print("Pasando de NUEVO a PREPARANDO")
        pedido.estado = "preparando"

    def cancelar(self, pedido):
        print("Pedido cancelado desde estado NUEVO")
        pedido.estado = "cancelado"


class EstadoPreparando(EstadoPedido):
    def avanzar(self, pedido):
        print("Pasando de PREPARANDO a LISTO")
        pedido.estado = "listo"

    def cancelar(self, pedido):
        print("Pedido cancelado desde estado PREPARANDO")
        pedido.estado = "cancelado"


class EstadoListo(EstadoPedido):
    def avanzar(self, pedido):
        print("Pasando de LISTO a ENTREGADO")
        pedido.estado = "entregado"

    def cancelar(self, pedido):
        print("Pedido ya está listo. No puede cancelarse.")


class EstadoEntregado(EstadoPedido):
    def avanzar(self, pedido):
        print("El pedido ya fue ENTREGADO. No hay más transiciones.")

    def cancelar(self, pedido):
        print("No se puede cancelar un pedido ya ENTREGADO.")


class EstadoCancelado(EstadoPedido):
    def avanzar(self, pedido):
        print("El pedido está CANCELADO. No puede avanzar.")

    def cancelar(self, pedido):
        print("El pedido ya está cancelado.")


def obtener_estado_instancia(nombre_estado):
    estados = {
        "nuevo": EstadoNuevo(),
        "preparando": EstadoPreparando(),
        "listo": EstadoListo(),
        "entregado": EstadoEntregado(),
        "cancelado": EstadoCancelado()
    }
    return estados.get(nombre_estado, EstadoNuevo())
