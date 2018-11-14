#ifndef RIDERPAGE_H
#define RIDERPAGE_H

#include <QDialog>

namespace Ui {
class RiderPage;
}

class RiderPage : public QDialog
{
    Q_OBJECT

public:
    explicit RiderPage(QWidget *parent = nullptr);
    ~RiderPage();

private:
    Ui::RiderPage *ui;
};

#endif // RIDERPAGE_H
