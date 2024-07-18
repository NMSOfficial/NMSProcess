#include <QApplication>
#include "ana_pencere.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    AnaPencere pencere;
    pencere.show();
    return app.exec();
}

