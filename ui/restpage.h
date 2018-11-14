#ifndef RESTPAGE_H
#define RESTPAGE_H

#include <QDialog>

namespace Ui {
class RestPage;
}

class RestPage : public QDialog
{
    Q_OBJECT

public:
    explicit RestPage(QWidget *parent = nullptr);
    ~RestPage();

private:
    Ui::RestPage *ui;
};

#endif // RESTPAGE_H
